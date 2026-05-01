# Task Manager

Un gestor de tareas inteligente con interfaz de línea de comandos que permite crear, listar, completar y eliminar tareas. Incluye una funcionalidad avanzada de IA que desglosa tareas complejas en subtareas simples usando la API de OpenAI.

## 🌟 Características

- ✅ **Gestión básica de tareas**: Crear, listar, completar y eliminar tareas
- 🤖 **Desglose inteligente**: Utiliza IA (OpenAI) para convertir tareas complejas en subtareas accionables
- 💾 **Persistencia**: Guarda todas las tareas en formato JSON
- 🎯 **ID automático**: Asignación automática de IDs únicos a cada tarea
- 📋 **Estado visual**: Indicadores visuales (✓) para tareas completadas
- 🧪 **Pruebas completas**: Suite de 25 tests unitarios con cobertura total

## 📋 Requisitos

- Python 3.8 o superior
- OpenAI API key (para la funcionalidad de IA)

## 📦 Dependencias

```
openai==2.33.0
python-dotenv==1.2.2
```

Para ver todas las dependencias, consulta [requirements.txt](requirements.txt)

## 🚀 Instalación

### 1. Clonar o descargar el proyecto
```bash
cd taskmanager
```

### 2. Crear un entorno virtual
```bash
python -m venv .venv
source .venv/bin/activate  # En macOS/Linux
# o
.venv\Scripts\activate  # En Windows
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar la API de OpenAI
Crea un archivo `.env` en la raíz del proyecto:
```
OPENAI_API_KEY=tu_api_key_aqui
```

## 💻 Uso

### Ejecutar la aplicación
```bash
python main.py
```

### Menú principal
```
--- Task Manager ---
1. Add task
2. Add complex task
3. List tasks
4. Complete task
5. Remove task
6. Exit
```

### Ejemplos de uso

#### 1. Agregar una tarea simple
```
Choose an option: 1
Task name: Buy groceries
Task description: Get milk and eggs
Task added: Buy groceries
```

#### 2. Agregar una tarea compleja (con IA)
```
Choose an option: 2
Task complex name: Plan holiday trip
Task complex description: Plan a 2-week vacation to Europe including flights, hotels, and activities
```
La IA desglosa esto en 3-5 subtareas simples como:
- Research destinations and flight options
- Book flights and accommodations
- Plan daily activities and attractions
- Arrange travel insurance and visas
- Create packing list and prepare luggage

#### 3. Listar tareas
```
Choose an option: 3
[ ] #1: Buy groceries
[ ] #2: Research destinations and flight options
[ ] #3: Book flights and accommodations
```

#### 4. Completar una tarea
```
Choose an option: 4
Task id to complete: 1
Task completed: Buy groceries
```

#### 5. Eliminar una tarea
```
Choose an option: 5
Task id to delete: 1
Task removed: 1
```

## 📁 Estructura del proyecto

```
taskmanager/
├── task_manager.py          # Clases Task y TaskManager
├── ai_service.py            # Servicio de IA para generar subtareas
├── main.py                  # Interfaz principal de línea de comandos
├── tasks.json               # Base de datos de tareas (se crea automáticamente)
├── requirements.txt         # Dependencias del proyecto
├── .env                     # Variables de entorno (no incluido en el repo)
├── .venv/                   # Entorno virtual
├── test_task_manager.py     # Tests para TaskManager
├── test_ai_service.py       # Tests para el servicio de IA
├── test_main.py             # Tests para la interfaz principal
└── README.md                # Este archivo
```

## 🏗️ Arquitectura

### Clases principales

#### `Task`
Representa una tarea individual con propiedades:
- `id`: Identificador único
- `name`: Nombre de la tarea
- `description`: Descripción detallada
- `completed`: Estado (completada o no)

#### `TaskManager`
Gestor central de tareas con métodos:
- `add_task(name, description)`: Agregar nueva tarea
- `list_task()`: Listar todas las tareas
- `complete_task(id)`: Marcar tarea como completada
- `delete_task(id)`: Eliminar una tarea
- `load_tasks()`: Cargar tareas del archivo JSON
- `save_tasks()`: Guardar tareas en archivo JSON

#### `create_simple_tasks(description)`
Función que genera subtareas usando OpenAI:
- Acepta una descripción de tarea compleja
- Retorna una lista de 3-5 subtareas simples
- Maneja errores de API de forma elegante

## 🧪 Pruebas

El proyecto incluye una suite completa de 25 tests unitarios.

### Ejecutar todas las pruebas
```bash
python -m unittest discover -s . -p "test_*.py" -v
```

### Ejecutar pruebas específicas
```bash
# Solo tests de TaskManager
python -m unittest test_task_manager -v

# Solo tests del servicio de IA
python -m unittest test_ai_service -v

# Solo tests del menú principal
python -m unittest test_main -v
```

### Cobertura de tests

**test_task_manager.py** (13 tests)
- ✅ Creación de tareas
- ✅ Representación en string (incompleta/completada)
- ✅ Agregar tareas simples y múltiples
- ✅ Listar tareas (vacío/con datos)
- ✅ Completar tareas
- ✅ Eliminar tareas
- ✅ Cargar/guardar en archivo
- ✅ Gestión de IDs

**test_ai_service.py** (7 tests)
- ✅ Creación exitosa de subtareas
- ✅ Validación de API key
- ✅ Manejo de errores de conexión
- ✅ Respuestas vacías
- ✅ Parsing con espacios extra
- ✅ Múltiples subtareas
- ✅ Formato de prompt

**test_main.py** (2 tests)
- ✅ Impresión del menú
- ✅ Validación de opciones

## 🔧 Configuración

### Variables de entorno (.env)
```
OPENAI_API_KEY=sk-...  # Tu clave API de OpenAI
```

### Modelos y parámetros de IA (en ai_service.py)
```python
model="gpt-5.4-mini"           # Modelo de OpenAI a usar
max_completion_tokens=300      # Máximo de tokens
reasoning_effort="low"         # Esfuerzo de razonamiento bajo
```

## 📝 Formato de almacenamiento

Las tareas se guardan en formato JSON en `tasks.json`:
```json
[
    {
        "id": 1,
        "name": "Buy groceries",
        "description": "Get milk and eggs",
        "completed": false
    },
    {
        "id": 2,
        "name": "Write report",
        "description": "Complete quarterly report",
        "completed": true
    }
]
```

## ⚠️ Troubleshooting

### Error: "La API key de OpenAI no está configurada"
- Verifica que existe el archivo `.env` en la raíz del proyecto
- Asegúrate de que contiene una clave válida: `OPENAI_API_KEY=tu_clave`

### Error: "Error de conexión o parámetros"
- Verifica tu conexión a Internet
- Valida que tu API key sea correcta
- Revisa los límites de uso de tu cuenta OpenAI

### Las tareas no se guardan
- Verifica que tienes permisos de escritura en el directorio del proyecto
- Comprueba que `tasks.json` no está corrupto

## 📚 Referencias

- [OpenAI API Documentation](https://platform.openai.com/docs)
- [Python unittest Documentation](https://docs.python.org/3/library/unittest.html)
- [Python JSON Documentation](https://docs.python.org/3/library/json.html)

## 🤝 Contribuir

Las contribuciones son bienvenidas. Para cambios importantes:
1. Fork del proyecto
2. Crear una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo licencia MIT. Ver detalles en LICENSE.

## ✉️ Contacto

Para preguntas o sugerencias, abre un issue en el repositorio.

---

**Última actualización**: 1 de mayo de 2026
