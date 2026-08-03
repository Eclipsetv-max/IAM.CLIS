# -*- coding: utf-8 -*-
"""
IAM Model Evaluator
Evalua el rendimiento del modelo fine-tuned
"""

import json
import sys
import time
from pathlib import Path
from typing import List, Dict

sys.path.insert(0, str(Path(__file__).parent.parent.parent))


class IAMEvaluator:
    """Evaluador de modelos IAM"""

    # Preguntas de prueba por modo
    TEST_CASES = {
        "general": [
            {
                "input": "Crea un archivo hello.py con hola mundo",
                "expected_patterns": ["TOOL_CALL", "create_file", "hello.py"],
                "description": "Creacion basica de archivo",
            },
            {
                "input": "Que hora es?",
                "expected_patterns": ["hora", "sistema"],
                "description": "Pregunta basica del sistema",
            },
            {
                "input": "Lee el archivo main.py",
                "expected_patterns": ["TOOL_CALL", "read_file", "main.py"],
                "description": "Lectura de archivo",
            },
        ],
        "builder": [
            {
                "input": "Hazme una web basica con HTML, CSS y JS",
                "expected_patterns": ["TOOL_CALL", "create_file", "index.html", "style.css"],
                "description": "Creacion de proyecto web basico",
            },
            {
                "input": "Crea un boton con hover effect",
                "expected_patterns": [":hover", "transition", "background"],
                "description": "Estilos CSS especificos",
            },
        ],
        "debug": [
            {
                "input": "Tengo un error de sintaxis en mi codigo",
                "expected_patterns": ["TOOL_CALL", "read_file", "error", "linea"],
                "description": "Diagnostico de error",
            },
        ],
        "security": [
            {
                "input": "Revisa mi codigo por vulnerabilidades XSS",
                "expected_patterns": ["XSS", "sanitiz", "escape"],
                "description": "Analisis de seguridad",
            },
        ],
    }

    def __init__(self, model_path: str = None):
        self.model_path = model_path
        self.results: List[Dict] = []

    def evaluate_model(self, model_path: str = None, modes: List[str] = None):
        """Evaluar el modelo en todos los modos"""
        from iam.training.train import IAMTrainer

        if model_path:
            self.model_path = model_path

        if not self.model_path:
            print("[ERROR] No se ha especificado un modelo")
            return

        print("=" * 60)
        print("IAM Model Evaluator")
        print("=" * 60)
        print(f"Modelo: {self.model_path}")
        print()

        # Cargar modelo
        trainer = IAMTrainer(model_name="custom")
        trainer.model_path = self.model_path
        trainer.load_model(use_4bit=False)

        # Evaluar por modo
        if modes is None:
            modes = list(self.TEST_CASES.keys())

        for mode in modes:
            if mode in self.TEST_CASES:
                self._evaluate_mode(trainer, mode)

        # Resumen
        self._print_summary()

        return self.results

    def _evaluate_mode(self, trainer, mode: str):
        """Evaluar todas las pruebas de un modo"""
        test_cases = self.TEST_CASES.get(mode, [])
        
        print(f"\n--- Modo: {mode} ---")
        
        for i, test in enumerate(test_cases, 1):
            print(f"\n  [{i}/{len(test_cases)}] {test['description']}")
            print(f"  Input: {test['input'][:60]}...")
            
            # Generar respuesta
            start = time.time()
            response = trainer.generate(test["input"], max_new_tokens=256)
            elapsed = time.time() - start
            
            # Verificar patrones esperados
            response_lower = response.lower() if response else ""
            patterns_found = sum(
                1 for p in test["expected_patterns"]
                if p.lower() in response_lower
            )
            score = patterns_found / len(test["expected_patterns"])
            
            result = {
                "mode": mode,
                "input": test["input"],
                "response": response[:200] if response else "",
                "expected_patterns": test["expected_patterns"],
                "patterns_found": patterns_found,
                "total_patterns": len(test["expected_patterns"]),
                "score": score,
                "time": elapsed,
                "passed": score >= 0.5,
            }
            self.results.append(result)
            
            status = "PASS" if result["passed"] else "FAIL"
            print(f"  Score: {score:.0%} ({patterns_found}/{len(test['expected_patterns'])})")
            print(f"  Time: {elapsed:.1f}s | Status: {status}")
            print(f"  Response: {(response or '')[:100]}...")

    def _print_summary(self):
        """Imprimir resumen de evaluacion"""
        print("\n" + "=" * 60)
        print("RESUMEN DE EVALUACION")
        print("=" * 60)
        
        total = len(self.results)
        passed = sum(1 for r in self.results if r["passed"])
        avg_score = sum(r["score"] for r in self.results) / max(total, 1)
        avg_time = sum(r["time"] for r in self.results) / max(total, 1)
        
        # Por modo
        modes = {}
        for r in self.results:
            mode = r["mode"]
            if mode not in modes:
                modes[mode] = {"total": 0, "passed": 0, "scores": []}
            modes[mode]["total"] += 1
            if r["passed"]:
                modes[mode]["passed"] += 1
            modes[mode]["scores"].append(r["score"])
        
        print(f"\nTotal pruebas: {total}")
        print(f"Aprobadas: {passed} ({100*passed/max(total,1):.0f}%)")
        print(f"Score promedio: {avg_score:.0%}")
        print(f"Tiempo promedio: {avg_time:.1f}s")
        
        print("\nPor modo:")
        for mode, stats in modes.items():
            mode_avg = sum(stats["scores"]) / len(stats["scores"])
            print(f"  {mode}: {stats['passed']}/{stats['total']} ({mode_avg:.0%})")

    def save_results(self, filepath: str = None):
        """Guardar resultados en JSON"""
        if filepath is None:
            filepath = Path(__file__).parent / "evaluation_results.json"
        
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        
        print(f"\n[OK] Resultados guardados en: {filepath}")


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="IAM Model Evaluator")
    parser.add_argument("--model", required=True, help="Ruta al modelo fine-tuned")
    parser.add_argument("--modes", nargs="+", default=None,
                       help="Modos a evaluar (default: todos)")
    parser.add_argument("--save", default=None, help="Guardar resultados")
    
    args = parser.parse_args()
    
    evaluator = IAMEvaluator()
    evaluator.evaluate_model(model_path=args.model, modes=args.modes)
    
    if args.save:
        evaluator.save_results(args.save)


if __name__ == "__main__":
    main()
