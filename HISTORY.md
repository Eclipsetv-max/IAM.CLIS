# Historial de Cambios - IA

## v3.1.1 - 28/07/2026

### Mejoras en Apariencia

1. **`main.py` - Banner Actualizado**
   - Nuevo banner con panel "PLAN DE ACCIÓN" a la derecha
   - Sección "CONTEXTO DE OPERACIÓN" con puntos decorativos
   - Elemento de red (network mesh) en la esquina inferior derecha
   - Prompt de entrada estilo: `C:\IAM>iam/general |`

2. **`start.bat` y `start.ps1`**
   - Actualizados para reflejar el nuevo diseño del banner
   - Versión actualizada a 3.1.1

3. **`iam/config/settings.py`**
   - Versión actualizada a 3.1.1

4. **`README.md`**
   - Versión actualizada a 3.1.1

### Bugs Corregidos

1. **`iam/core/agent.py` - `_handle_command()`**
   - El comando completo se convertia a minusculas, incluyendo rutas y contenido de archivos
   - Ahora solo se convierte a minusculas el nombre del comando, no los argumentos

2. **`iam/core/agent.py` - `_call_groq()`**
   - Usaba modelos de OpenCode (`mimo-v2.5-free`) en vez de modelos Groq
   - Corregido para usar `settings.FALLBACK_MODELS["groq"]` con `llama-3.1-8b-instant`

3. **`iam/tools/filesystem.py`**
   - Faltaba `import platform` necesario para funciones `get_owner()` y `set_owner()`

4. **`iam/tools/system.py` - `get_memory_info()`**
   - `wmic` devolvia columnas en orden inverso
   - Habia lineas vacias entre el header y los datos
   - Ahora parsea el header para detectar el orden correcto y filtra lineas vacias

5. **Banner**
   - Cambiado a ASCII simple que funciona en cualquier terminal
   - Subtitulo: "Inteligencia Artificial Unida"

### Estado Actual

- Motor por defecto: **OpenCode** con modelo **mimo-v2.5-free**
- 74/74 tests pasando
- Todas las herramientas funcionando:
  - Sistema de archivos (crear, leer, editar, eliminar)
  - Informacion del sistema (CPU, RAM, disco, procesos)
  - Red (IP, ping, DNS, conexiones)
  - Hardware (GPU, bateria, USB)
  - Seguridad (firewall, usuarios, logs)
  - Ejecucion de codigo (Python, comandos)
  - Creacion de proyectos (calculadora, web, API, juegos, etc.)
  - Modos de IA (general, builder, plan, frontend, backend, debug, security)
  - Memoria a largo plazo
  - Gestion de sesiones
