# IAM v5.0 - Changelog y Documentacion

## Resumen de Cambios (Agosto 2026)

### Optimizaciones de Velocidad
- `MAX_CONTEXT_MESSAGES`: 20 → 8 (prompt 65% mas corto)
- `MAX_SESSION_MESSAGES`: 50 → 20
- Prompt enriquecido reducido de ~12,000 a ~4,000 chars
- Timeout proxy: 60s → 30s
- Max tokens: 2048 → 1024
- Reintentos automaticos: 3 → 1

### Bug Fixes
- Eliminado loader doble que causaba texto cortado en streaming
- Importacion faltante de `validate_file`
- F-strings con JSX corregidos

---

## 185 Acciones Disponibles

### Archivos y Carpetas (35)
| Accion | Descripcion |
|--------|-------------|
| `create_file` | Crear archivo |
| `create_files_batch` | Crear multiples archivos |
| `read_file` | Leer archivo |
| `read_file_lines` | Leer lineas especificas |
| `edit_file` | Editar archivo |
| `edit_file_line` | Editar linea especifica |
| `insert_in_file` | Insertar texto despues de patron |
| `append_to_file` | Agregar al final |
| `prepend_to_file` | Agregar al inicio |
| `delete_file` | Eliminar archivo |
| `delete_files` | Eliminar archivos por patron |
| `clear_folder` | Limpiar carpeta completa |
| `copy_file` | Copiar archivo/carpeta |
| `move_file` | Mover archivo |
| `rename_file` | Renombrar archivo |
| `create_folder` | Crear carpeta |
| `create_folders_batch` | Crear multiples carpetas |
| `remove_folder` | Eliminar carpeta |
| `empty_file` | Vaciar archivo |
| `get_file_info` | Obtener info del archivo |
| `list_directory` | Listar directorio |
| `tree_directory` | Mostrar estructura |
| `find_files` | Buscar archivos por patron |
| `find_files_by_extension` | Buscar por extension |
| `search_in_files` | Buscar texto en archivos |
| `replace_in_files` | Reemplazar texto en archivos |
| `count_lines` | Contar lineas |
| `count_lines_all` | Contar lineas totales |
| `file_hash` | Calcular hash |
| `compare_files` | Comparar archivos |
| `backup_file` | Crear backup |
| `restore_backup` | Restaurar backup |
| `make_readonly` | Solo lectura |
| `make_writable` | Hacer escribible |
| `get_size` | Obtener tamano |
| `touch_file` | Crear/actualizar timestamp |
| `symlink` | Crear enlace symbolico |
| `change_permissions` | Cambiar permisos |
| `find_duplicate_files` | Encontrar duplicados |
| `organize_files_by_extension` | Organizar por extension |
| `clean_empty_folders` | Eliminar carpetas vacias |
| `create_project_structure` | Crear estructura de proyecto |

### Git (19)
| Accion | Descripcion |
|--------|-------------|
| `git_init` | Inicializar repositorio |
| `git_add` | Agregar archivos |
| `git_commit` | Crear commit |
| `git_status` | Ver estado |
| `git_log` | Ver historial |
| `git_diff` | Ver diferencias |
| `git_branch` | Crear/listar branches |
| `git_checkout` | Cambiar branch |
| `git_merge` | Merge branch |
| `git_push` | Push a remote |
| `git_pull` | Pull de remote |
| `git_clone` | Clonar repositorio |
| `git_stash` | Stash cambios |
| `git_stash_pop` | Pop stash |
| `git_tag` | Crear tag |
| `git_revert` | Revert commit |
| `git_reset` | Reset commits |
| `git_remote_add` | Agregar remote |
| `git_ignore` | Agregar a .gitignore |

### Python (22)
| Accion | Descripcion |
|--------|-------------|
| `run_python` | Ejecutar codigo Python |
| `run_python_file` | Ejecutar archivo Python |
| `create_virtualenv` | Crear virtualenv |
| `install_package` | Instalar paquete |
| `install_requirements` | Instalar requirements |
| `freeze_requirements` | Guardar requirements |
| `list_packages` | Listar paquetes |
| `check_outdated` | Ver desactualizados |
| `uninstall_package` | Desinstalar paquete |
| `format_code` | Formatear codigo |
| `lint_code` | Verificar codigo |
| `type_check` | Verificar tipos |
| `run_tests` | Ejecutar tests |
| `create_module` | Crear modulo |
| `create_class` | Crear clase |
| `create_fastapi_endpoint` | Crear endpoint FastAPI |
| `create_flask_route` | Crear ruta Flask |
| `create_django_view` | Crear vista Django |
| `create_sqlalchemy_model` | Crear modelo SQLAlchemy |
| `create_pydantic_model` | Crear modelo Pydantic |
| `create_test_file` | Crear tests |
| `create_dockerfile_python` | Crear Dockerfile |
| `create_docker_compose` | Crear docker-compose |
| `create_github_workflow` | Crear workflow CI |

### Web y Frontend (18)
| Accion | Descripcion |
|--------|-------------|
| `create_html_page` | Crear pagina HTML |
| `create_react_component` | Crear componente React |
| `create_vue_component` | Crear componente Vue |
| `create_angular_component` | Crear componente Angular |
| `create_svelte_component` | Crear componente Svelte |
| `create_nextjs_page` | Crear pagina Next.js |
| `create_api_endpoint_express` | Crear endpoint Express |
| `create_package_json` | Crear package.json |
| `create_vite_config` | Crear vite.config.js |
| `create_tailwind_config` | Crear tailwind.config.js |
| `create_responsive_css` | CSS responsive |
| `create_animation_css` | CSS con animaciones |
| `create_dark_mode_css` | CSS dark mode |
| `create_glassmorphism_css` | CSS glassmorphism |
| `create_gradient_css` | CSS gradientes |
| `create_grid_layout` | CSS grid layout |
| `create_flexbox_layout` | CSS flexbox |
| `create_utilities_css` | CSS utilidades |

### Base de Datos (7)
| Accion | Descripcion |
|--------|-------------|
| `create_sqlite_db` | Crear SQLite |
| `create_postgres_db` | Crear PostgreSQL |
| `create_mongo_collection` | Crear coleccion MongoDB |
| `sql_query` | Ejecutar SQL |
| `create_migration` | Crear migracion |
| `create_seed_data` | Crear datos seed |
| `backup_database` | Backup de DB |

### Red y APIs (12)
| Accion | Descripcion |
|--------|-------------|
| `http_get` | GET request |
| `http_post` | POST request |
| `http_put` | PUT request |
| `http_delete` | DELETE request |
| `download_file` | Descargar archivo |
| `upload_file` | Subir archivo |
| `create_api_server` | Crear servidor API |
| `create_rest_api` | Crear API REST completa |
| `create_websocket_server` | Crear WebSocket |
| `create_grpc_service` | Crear servicio gRPC |
| `create_middleware` | Crear middleware |
| `create_rate_limiter` | Crear rate limiter |

### Seguridad (11)
| Accion | Descripcion |
|--------|-------------|
| `generate_password` | Generar contrasena |
| `generate_api_key` | Generar API key |
| `generate_jwt_secret` | Generar JWT secret |
| `hash_password` | Hashear contrasena |
| `verify_password` | Verificar contrasena |
| `encrypt_text` | Cifrar texto |
| `decrypt_text` | Descifrar texto |
| `scan_ports` | Escanear puertos |
| `create_ssl_cert` | Crear certificado SSL |
| `validate_input` | Validar input |
| `sanitize_filename` | Sanitizar nombre |

### Sistema (11)
| Accion | Descripcion |
|--------|-------------|
| `get_system_info` | Info del sistema |
| `get_cpu_info` | Info CPU |
| `get_memory_info` | Info memoria |
| `get_disk_info` | Info disco |
| `get_process_list` | Listar procesos |
| `kill_process` | Matar proceso |
| `set_environment_variable` | Configurar env |
| `get_environment_variables` | Obtener envs |
| `create_cron_job` | Crear cron job |
| `schedule_task` | Programar tarea |

### Multimedia (4)
| Accion | Descripcion |
|--------|-------------|
| `create_image` | Crear imagen |
| `resize_image` | Redimensionar |
| `convert_image` | Convertir formato |
| `create_qr_code` | Crear codigo QR |

### Documentacion (4)
| Accion | Descripcion |
|--------|-------------|
| `create_readme` | Crear README |
| `create_documentation` | Crear docs de API |
| `create_changelog` | Crear changelog |
| `create_api_docs_openapi` | Crear OpenAPI |

### Testing (5)
| Accion | Descripcion |
|--------|-------------|
| `create_unit_test` | Crear test unitario |
| `create_integration_test` | Crear test integracion |
| `create_mock` | Crear mock |
| `create_fixtures` | Crear fixtures |
| `create_benchmark` | Crear benchmark |

### Utilidades (24)
| Accion | Descripcion |
|--------|-------------|
| `timestamp` | Obtener timestamp |
| `format_date` | Formatear fecha |
| `days_between` | Dias entre fechas |
| `add_days` | Agregar dias |
| `generate_uuid` | Generar UUID |
| `generate_random_string` | String aleatorio |
| `generate_random_number` | Numero aleatorio |
| `slugify` | Convertir a slug |
| `truncate` | Truncar texto |
| `word_count` | Contar palabras |
| `pretty_json` | Formatear JSON |
| `csv_to_json` | CSV a JSON |
| `json_to_csv` | JSON a CSV |
| `create_env_file` | Crear .env |
| `parse_env_file` | Leer .env |
| `create_gitignore` | Crear .gitignore |
| `create_editorconfig` | Crear .editorconfig |
| `create_prettier_config` | Crear .prettierrc |
| `create_eslint_config` | Crear .eslintrc |
| `create_tsconfig` | Crear tsconfig.json |
| `create_postman_collection` | Crear Postman |
| `create_swagger_ui` | Crear Swagger UI |
| `create_makefile` | Crear Makefile |
| `create_dockerignore` | Crear .dockerignore |
| `create_procfile` | Crear Procfile |
| `create_terraform_config` | Crear Terraform |
| `create_kubernetes_deployment` | Crear K8s Deployment |
| `create_ansible_playbook` | Crear Ansible |
| `create_github_actions_ci` | Crear CI workflow |

---

## Comportamiento Mejorado

### IA Ejecuta Todo de Una Vez
La IA ahora genera TODOS los TOOL_CALLs necesarios en una sola respuesta. Si pides "elimina todo", ejecuta `clear_folder` directamente sin detenerse.

### IA Sugiere Siguientes Pasos
Despues de cada accion, la IA sugiere que hacer despues:
- **Archivos creados:** "Abrir", "Ejecutar", "Editar"
- **Eliminacion:** "Crear nuevos archivos", "Listar carpeta"
- **Errores:** "Revisar error", "Reintentar"
- **Web:** "Abrir en navegador", "Agregar estilos"
- **Python:** "Ejecutar script", "Crear tests"

### Categorias de Sugerencias
1. `create_file` - Para archivos creados
2. `delete` - Para eliminaciones
3. `clear_folder` - Para limpiar carpetas
4. `error` - Para errores
5. `code` - Para codigo
6. `git` - Para operaciones git
7. `web` - Para proyectos web
8. `python` - Para Python
9. `question` - Para preguntas
10. `success` - Para exitos generales

---

## Ejemplos de Uso

### Eliminar todo el contenido
```
Usuario: elimina todo lo que hay dentro de la carpeta
IA: [TOOL_CALL] action: clear_folder path: "C:\Users\usuario\proyecto"
[/TOOL_CALL]
Listo! Carpeta limpiada. Puedo:
1) Crear nuevo proyecto
2) Listar carpeta vacia
3) Verificar contenido
```

### Crear proyecto completo
```
Usuario: crea un proyecto web con HTML, CSS y JS
IA: [TOOL_CALL] action: create_file name: "index.html"
<!DOCTYPE html>...
[/TOOL_CALL]

[TOOL_CALL] action: create_file name: "style.css"
/* styles */
[/TOOL_CALL]

[TOOL_CALL] action: create_file name: "script.js"
// code
[/TOOL_CALL]

Proyecto creado! Puedo:
1) Abrir en navegador
2) Agregar mas estilos
3) Crear mas paginas
```

### Ejecutar Python
```
Usuario: ejecuta este codigo: print("Hola")
IA: [TOOL_CALL] action: run_python command: "print('Hola')"
[/TOOL_CALL]
Hola
Puedo:
1) Ejecutar script
2) Crear tests
3) Instalar dependencias
```

---

## Archivos Modificados

- `iam/config/settings.py` - Optimizaciones de velocidad
- `iam/config/prompts.py` - Nuevas instrucciones para IA
- `iam/core/agent.py` - Integracion de acciones avanzadas
- `iam/core/enhanced_cli.py` - Mejoras en sugerencias
- `iam/tools/advanced_actions.py` - 185 nuevas acciones

---

## Commits Recientes

| Hash | Descripcion |
|------|-------------|
| `1096c4f` | fix: IA ejecuta todo de una vez y sugiere siguientes pasos |
| `10e9ee7` | feat: 185 acciones avanzadas |
| `f0da131` | feat: 15 acciones basicas |
| `18dda48` | feat: accion clear_folder |
| `6a56185` | fix: importar validate_file |
| `f006107` | fix: eliminar loader doble |
| `8f5b4d4` | perf: optimizar velocidad |

---

## Notas para Mañana

1. **Probar todas las acciones** - Ejecutar cada accion para verificar que funciona
2. **Agregar mas acciones** - Si faltan acciones especificas, agregarlas
3. **Mejorar prompts** - Ajustar instrucciones segun comportamiento observado
4. **Documentar APIs** - Crear documentacion de las APIs disponibles
5. **Testing** - Crear tests para todas las acciones
