# IAM v3.0.0 - Intencional Artificial Multitarea
## Documentacion del Proyecto
### Ultima actualizacion: 27 de julio, 2026

---

## Resumen
IAM es un asistente de IA personal. Un sistema completo que incluye:
- Chat con IA (Groq/Hugging Face)
- Control total del PC
- Monitoreo de pantalla
- Gestion de codigo y archivos
- Busquedas web y JW.org

---

## Arquitectura

```
iam/
├── main.py              # Punto de entrada
├── config/
│   ├── settings.py      # Configuracion global
│   └── prompts.py       # System prompts
├── core/
│   ├── session.py       # Gestion de sesiones
│   └── agent.py         # Agente de IA
├── tools/
│   ├── screen.py        # Monitoreo de pantalla
│   ├── apps.py          # Control de aplicaciones
│   ├── code.py          # Gestion de codigo
│   ├── search.py        # Busquedas
│   └── system.py        # Info del sistema
└── data/                # Datos persistentes
```

---

## Modos/Agentes

| Modo | Icono | Descripcion |
|------|-------|-------------|
| general | ☁ | Asistente general |
| builder | ⚒ | Crear proyectos |
| plan | ☑ | Planificacion |
| frontend | ▣ | UI/UX y frontend |
| backend | ⚙ | APIs y backend |
| debug | ⚒ | Encontrar bugs |

---

## Comandos

| Comando | Descripcion |
|---------|-------------|
| `/help` | Ver ayuda |
| `/status` | Estado del sistema |
| `/mode [m]` | Cambiar modo |
| `/engine [e]` | Cambiar motor IA |
| `/sessions` | Listar sesiones |
| `/new [name]` | Nueva sesion |
| `/jw [query]` | Buscar en JW.org |

---

## Motores de IA

### OpenCode (Motor Principal)
- **URL**: opencode.ai
- **Costo**: Tier gratuito disponible
- **Velocidad**: Rapida
- **Modelos**: MiMo v2.5, DeepSeek, Kimi, GLM

### Groq (Fallback)
- **URL**: console.groq.com
- **Costo**: Gratis
- **Velocidad**: Ultra rapido

### Hugging Face
- **URL**: huggingface.co
- **Costo**: Gratis
- **Velocidad**: Normal

---

## Tecnologias

### Backend
- Python 3.10+
- requests (APIs)
- subprocess (sistema)

### APIs
- Groq API (IA)
- Hugging Face API (IA)

### Dependencias
```bash
pip install -r requirements.txt
```

---

## Soporte

Si hay problemas:
1. Ejecutar `/status` para verificar conexiones
2. Verificar internet si IA no responde
3. Reiniciar terminal si hay errores

---

*Sistema IAM v3.0.0*
