# -*- coding: utf-8 -*-
"""
IAM Local Model Loader
Carga y usa modelos fine-tuned localmente
"""

import os
import sys
import json
import torch
from pathlib import Path
from typing import Optional, Dict, Any

sys.path.insert(0, str(Path(__file__).parent.parent.parent))


class IAMLocalModel:
    """Cargador de modelos IAM fine-tuned"""

    def __init__(self, model_path: str = None):
        self.model_path = model_path
        self.model = None
        self.tokenizer = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self._loaded = False

    def load(self, model_path: str = None):
        """Cargar modelo desde disco"""
        from transformers import AutoModelForCausalLM, AutoTokenizer

        if model_path:
            self.model_path = model_path

        if not self.model_path:
            raise ValueError("No se ha especificado ruta del modelo")

        model_path = Path(self.model_path)
        if not model_path.exists():
            raise FileNotFoundError(f"Modelo no encontrado: {model_path}")

        print(f"[IAM] Cargando modelo local: {model_path}")

        # Cargar tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(
            str(model_path),
            trust_remote_code=True,
        )

        # Cargar modelo
        self.model = AutoModelForCausalLM.from_pretrained(
            str(model_path),
            device_map="auto",
            trust_remote_code=True,
            torch_dtype=torch.float16,
        )

        self._loaded = True
        print(f"[IAM] Modelo cargado en {self.device}")

    def is_available(self) -> bool:
        """Verificar si el modelo esta cargado"""
        return self._loaded and self.model is not None

    def generate(
        self,
        prompt: str,
        system_prompt: str = None,
        max_new_tokens: int = 1024,
        temperature: float = 0.7,
        top_p: float = 0.9,
    ) -> str:
        """Generar respuesta con el modelo"""
        if not self.is_available():
            return None

        # Construir mensajes
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        else:
            messages.append({
                "role": "system",
                "content": "Tu eres IAM, un asistente de IA experto en programacion que ejecuta codigo directamente.",
            })
        messages.append({"role": "user", "content": prompt})

        # Aplicar chat template
        if hasattr(self.tokenizer, "apply_chat_template"):
            text = self.tokenizer.apply_chat_template(
                messages,
                tokenize=False,
                add_generation_prompt=True,
            )
        else:
            text = f"<|user|>\n{prompt}\n<|assistant|>\n"

        # Tokenizar
        inputs = self.tokenizer(text, return_tensors="pt").to(self.device)

        # Generar
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=max_new_tokens,
                temperature=temperature,
                top_p=top_p,
                do_sample=True,
                pad_token_id=self.tokenizer.eos_token_id,
            )

        # Decodificar
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)

        # Extraer solo la respuesta del asistente
        if "<|assistant|>" in response:
            response = response.split("<|assistant|>")[-1].strip()

        return response

    def unload(self):
        """Descargar modelo de memoria"""
        if self.model is not None:
            del self.model
            self.model = None
        if self.tokenizer is not None:
            del self.tokenizer
            self.tokenizer = None
        
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
        
        self._loaded = False
        print("[IAM] Modelo descargado")


def find_local_models() -> list:
    """Buscar modelos IAM fine-tuned disponibles"""
    models_dir = Path(__file__).parent / "models"
    models = []
    
    if models_dir.exists():
        for model_dir in models_dir.iterdir():
            if model_dir.is_dir():
                # Verificar que tiene archivos de modelo
                has_model = any(model_dir.glob("*.safetensors")) or \
                           any(model_dir.glob("*.bin")) or \
                           any(model_dir.glob("*.pt"))
                has_tokenizer = (model_dir / "tokenizer.json").exists() or \
                               (model_dir / "tokenizer_config.json").exists()
                
                if has_model and has_tokenizer:
                    # Leer metadata si existe
                    metadata = {}
                    metadata_file = model_dir / "metadata.json"
                    if metadata_file.exists():
                        with open(metadata_file) as f:
                            metadata = json.load(f)
                    
                    models.append({
                        "name": model_dir.name,
                        "path": str(model_dir),
                        "base_model": metadata.get("base_model", "unknown"),
                        "trained_at": metadata.get("trained_at", "unknown"),
                    })
    
    return models


def main():
    """CLI para probar el modelo local"""
    import argparse
    
    parser = argparse.ArgumentParser(description="IAM Local Model")
    parser.add_argument("--model", required=True, help="Ruta al modelo")
    parser.add_argument("--prompt", default="Crea un archivo hello.py", help="Prompt de prueba")
    parser.add_argument("--list", action="store_true", help="Listar modelos disponibles")
    
    args = parser.parse_args()
    
    if args.list:
        models = find_local_models()
        if models:
            print("Modelos IAM disponibles:")
            for m in models:
                print(f"  - {m['name']}: {m['base_model']} ({m['trained_at']})")
        else:
            print("No hay modelos entrenados. Ejecuta: python iam/training/train.py")
        return
    
    # Cargar y probar modelo
    local_model = IAMLocalModel()
    local_model.load(args.model)
    
    print(f"\nPrompt: {args.prompt}")
    print("-" * 40)
    
    response = local_model.generate(args.prompt)
    print(f"Respuesta:\n{response}")
    
    local_model.unload()


if __name__ == "__main__":
    main()
