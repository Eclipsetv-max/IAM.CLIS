# -*- coding: utf-8 -*-
"""
IAM Fine-Tuning Script
Entrena un modelo pequeño (TinyLlama) con QLoRA usando datos de IAM
"""

import os
import sys
import json
import torch
from pathlib import Path
from datetime import datetime

# Agregar directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))


class IAMTrainer:
    """Entrenador de modelo IAM con QLoRA"""

    # Modelos soportados (ordenados por tamaño)
    MODELS = {
        "tinyllama": "TinyLlama/TinyLlama-1.1B-Chat-v1.0",
        "phi2": "microsoft/phi-2",
        "gemma2b": "google/gemma-2b-it",
        "qwen0.5b": "Qwen/Qwen2-0.5B-Instruct",
        "smollm135m": "HuggingFaceTB/SmolLM-135M-Instruct",
    }

    def __init__(self, model_name: str = "tinyllama", output_dir: str = None):
        self.model_name = model_name
        self.model_path = self.MODELS.get(model_name, model_name)
        
        if output_dir is None:
            output_dir = Path(__file__).parent / "models" / model_name
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.model = None
        self.tokenizer = None
        self.trainer = None

    def load_model(self, use_4bit: bool = True):
        """Cargar modelo con QLoRA (4-bit)"""
        from transformers import (
            AutoModelForCausalLM,
            AutoTokenizer,
            BitsAndBytesConfig,
        )
        from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training

        print(f"[1/4] Cargando modelo: {self.model_path}")

        # Configuración 4-bit para QLoRA
        if use_4bit:
            bnb_config = BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_quant_type="nf4",
                bnb_4bit_compute_dtype=torch.float16,
                bnb_4bit_use_double_quant=True,
            )
        else:
            bnb_config = None

        # Cargar tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(
            self.model_path,
            trust_remote_code=True,
        )
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token

        # Cargar modelo
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_path,
            quantization_config=bnb_config,
            device_map="auto",
            trust_remote_code=True,
            torch_dtype=torch.float16,
        )

        # Preparar para entrenamiento
        if use_4bit:
            self.model = prepare_model_for_kbit_training(self.model)

        # Configurar LoRA
        lora_config = LoraConfig(
            r=16,
            lora_alpha=32,
            target_modules=[
                "q_proj", "k_proj", "v_proj", "o_proj",
                "gate_proj", "up_proj", "down_proj",
            ],
            lora_dropout=0.05,
            bias="none",
            task_type="CAUSAL_LM",
        )

        self.model = get_peft_model(self.model, lora_config)
        
        trainable, total = self.model.get_nb_trainable_parameters()
        print(f"  Parametros entrenables: {trainable:,} / {total:,} ({100*trainable/total:.2f}%)")

        return self.model

    def load_data(self, data_path: str = None):
        """Cargar datos de entrenamiento"""
        from datasets import load_dataset

        if data_path is None:
            data_path = Path(__file__).parent / "data" / "training_data.jsonl"
        
        data_path = Path(data_path)
        if not data_path.exists():
            print(f"[ERROR] Datos no encontrados: {data_path}")
            print("  Ejecuta primero: python iam/training/collect_data.py")
            return None

        print(f"[2/4] Cargando datos desde: {data_path}")

        dataset = load_dataset("json", data_files=str(data_path), split="train")
        print(f"  Ejemplos cargados: {len(dataset)}")

        # Formatear datos con chat template
        def format_example(example):
            messages = example["messages"]
            
            # Usar chat template del tokenizer
            if hasattr(self.tokenizer, "apply_chat_template"):
                text = self.tokenizer.apply_chat_template(
                    messages,
                    tokenize=False,
                    add_generation_prompt=False,
                )
            else:
                # Formato manual si el tokenizer no tiene chat template
                text = ""
                for msg in messages:
                    role = msg["role"]
                    content = msg["content"]
                    if role == "system":
                        text += f"<|system|>\n{content}\n"
                    elif role == "user":
                        text += f"<|user|>\n{content}\n"
                    elif role == "assistant":
                        text += f"<|assistant|>\n{content}\n"
                text += "<|assistant|>\n"

            return {"text": text}

        dataset = dataset.map(format_example, remove_columns=dataset.column_names)
        
        # Dividir train/eval
        split = dataset.train_test_split(test_size=0.1, seed=42)
        print(f"  Train: {len(split['train'])} | Eval: {len(split['test'])}")

        return split

    def train(self, data_path: str = None, epochs: int = 3, lr: float = 2e-4, batch_size: int = 2):
        """Entrenar el modelo"""
        from transformers import TrainingArguments, Trainer, DataCollatorForLanguageModeling

        # Cargar modelo y datos
        self.load_model(use_4bit=True)
        data = self.load_data(data_path)
        
        if data is None:
            return

        print(f"[3/4] Configurando entrenamiento...")

        # Configuración de entrenamiento
        training_args = TrainingArguments(
            output_dir=str(self.output_dir),
            num_train_epochs=epochs,
            per_device_train_batch_size=batch_size,
            per_device_eval_batch_size=batch_size,
            gradient_accumulation_steps=4,
            learning_rate=lr,
            weight_decay=0.01,
            warmup_ratio=0.03,
            lr_scheduler_type="cosine",
            logging_steps=10,
            eval_strategy="steps",
            eval_steps=50,
            save_strategy="steps",
            save_steps=100,
            save_total_limit=3,
            load_best_model_at_end=True,
            metric_for_best_model="eval_loss",
            greater_is_better=False,
            fp16=True,
            dataloader_num_workers=0,
            report_to="none",
            optim="paged_adamw_8bit",
            max_grad_norm=0.3,
            group_by_length=True,
        )

        # Data collator
        data_collator = DataCollatorForLanguageModeling(
            tokenizer=self.tokenizer,
            mlm=False,
        )

        # Trainer
        self.trainer = Trainer(
            model=self.model,
            args=training_args,
            train_dataset=data["train"],
            eval_dataset=data["test"],
            data_collator=data_collator,
        )

        print(f"[4/4] Entrenando...")
        print(f"  Epocas: {epochs}")
        print(f"  Learning rate: {lr}")
        print(f"  Batch size: {batch_size}")
        print(f"  Gradient accumulation: 4")
        print(f"  Total steps: {len(data['train']) // batch_size * epochs // 4}")
        print()

        # Entrenar
        start_time = datetime.now()
        self.trainer.train()
        elapsed = datetime.now() - start_time

        print()
        print(f"[OK] Entrenamiento completado en {elapsed}")
        
        # Guardar modelo
        self.save_model()
        
        return self.trainer

    def save_model(self):
        """Guardar modelo fine-tuned"""
        print(f"[OK] Guardando modelo en: {self.output_dir}")
        
        self.model.save_pretrained(str(self.output_dir))
        self.tokenizer.save_pretrained(str(self.output_dir))
        
        # Guardar metadata
        metadata = {
            "base_model": self.model_path,
            "model_name": self.model_name,
            "trained_at": datetime.now().isoformat(),
            "lora_rank": 16,
            "quantization": "4bit",
        }
        
        with open(self.output_dir / "metadata.json", "w") as f:
            json.dump(metadata, f, indent=2)
        
        print(f"[OK] Modelo guardado correctamente")

    def generate(self, prompt: str, max_new_tokens: int = 512, temperature: float = 0.7):
        """Generar respuesta con el modelo fine-tuned"""
        if self.model is None or self.tokenizer is None:
            print("[ERROR] Modelo no cargado. Usa load_model() primero.")
            return None

        # Formatear prompt
        messages = [
            {"role": "system", "content": "Tu eres IAM, un asistente de IA experto en programacion."},
            {"role": "user", "content": prompt},
        ]

        if hasattr(self.tokenizer, "apply_chat_template"):
            text = self.tokenizer.apply_chat_template(
                messages,
                tokenize=False,
                add_generation_prompt=True,
            )
        else:
            text = f"<|user|>\n{prompt}\n<|assistant|>\n"

        inputs = self.tokenizer(text, return_tensors="pt").to(self.model.device)
        
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=max_new_tokens,
                temperature=temperature,
                top_p=0.9,
                do_sample=True,
                pad_token_id=self.tokenizer.eos_token_id,
            )
        
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        # Extraer solo la respuesta del asistente
        if "<|assistant|>" in response:
            response = response.split("<|assistant|>")[-1].strip()
        
        return response


def main():
    """Función principal de entrenamiento"""
    import argparse
    
    parser = argparse.ArgumentParser(description="IAM Fine-Tuning")
    parser.add_argument("--model", default="tinyllama", 
                       choices=list(IAMTrainer.MODELS.keys()),
                       help="Modelo a entrenar")
    parser.add_argument("--data", default=None,
                       help="Ruta al archivo de datos JSONL")
    parser.add_argument("--epochs", type=int, default=3,
                       help="Numero de epocas")
    parser.add_argument("--lr", type=float, default=2e-4,
                       help="Learning rate")
    parser.add_argument("--batch-size", type=int, default=2,
                       help="Batch size")
    parser.add_argument("--collect-data", action="store_true",
                       help="Recolectar datos primero")
    parser.add_argument("--generate", type=str, default=None,
                       help="Generar respuesta con el modelo entrenado")
    
    args = parser.parse_args()
    
    # Recolectar datos si se pide
    if args.collect_data:
        from collect_data import collect_all
        collect_all()
        return
    
    # Crear trainer
    trainer = IAMTrainer(model_name=args.model)
    
    # Generar respuesta si se pide
    if args.generate:
        trainer.load_model(use_4bit=False)
        response = trainer.generate(args.generate)
        print(f"\nRespuesta:\n{response}")
        return
    
    # Entrenar
    trainer.train(
        data_path=args.data,
        epochs=args.epochs,
        lr=args.lr,
        batch_size=args.batch_size,
    )


if __name__ == "__main__":
    main()
