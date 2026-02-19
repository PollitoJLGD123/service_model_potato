# Potato Disease Classification API

API REST para clasificación de enfermedades de la papa usando TensorFlow/Keras. Desarrollada con FastAPI, Tortoise ORM y autenticación JWT.

## Requisitos Previos

- Python 3.12+
- PostgreSQL 12+
- pip o pipenv

## Instalación

1. Clonar el repositorio y entrar al directorio:
```bash
cd service_model
```

2. Crear entorno virtual:
```bash
python -m venv venv
```

3. Activar entorno virtual:
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

4. Instalar dependencias:
```bash
pip install -r requirements.txt
```

## Configuración

1. Crear archivo `.env` en la raíz del proyecto:
```env
PORT=4000
DEBUG=True
ENV=development

DB_HOST=localhost
DB_PORT=5432
DB_USER=postgres
DB_PASSWORD=root
DB_NAME=db_model_potato

JWT_SECRET="tu_secret_key_aqui"
JWT_EXPIRATION=3600

DOMAIN=.localhost
NAME_COOKIE=token_access
```

2. Asegurarse de que PostgreSQL esté corriendo y crear la base de datos:
```sql
CREATE DATABASE db_model_potato;
```

## Estructura del Proyecto

```
service_model/
├── src/
│   ├── config/          # Configuraciones (DB, JWT, Tortoise)
│   ├── controllers/     # Endpoints de la API
│   ├── database/        # Conexión y seeders
│   ├── helpers/         # Funciones auxiliares
│   ├── lib/             # Utilidades (JWT, bcrypt)
│   ├── middleware/      # Middleware de autenticación JWT
│   ├── models/          # Modelos de DB y ML (classifier)
│   ├── schemas/         # Esquemas Pydantic para validación
│   └── services/        # Lógica de negocio
├── model/               # Modelo entrenado (.keras) y métricas
├── main.py              # Punto de entrada
├── seed.py              # Script para poblar DB
└── requirements.txt     # Dependencias
```

## Ejecución

1. Poblar la base de datos (opcional, solo primera vez):
```bash
python seed.py
```

2. Iniciar el servidor:
```bash
python main.py
```

3. La API estará disponible en: `http://localhost:4000`

4. Documentación interactiva:
   - Swagger UI: `http://localhost:4000/docs`
   - ReDoc: `http://localhost:4000/redoc`

## Endpoints Principales

### Autenticación (Públicos)
- `POST /api/v1/login` - Iniciar sesión
  ```json
  {
    "email": "usuario@ejemplo.com",
    "password": "123456"
  }
  ```

### Evaluación (Protegido)
- `POST /api/v1/evaluation/evaluate` - Clasificar imagen de papa
  - Form-data: `file` (imagen)
  - Header: `Authorization: Bearer <token>`

### Entrenamiento (Protegido)
- `POST /api/v1/train/*` - Endpoints de entrenamiento del modelo

## Autenticación

Todas las rutas excepto `/login` requieren autenticación JWT.

**Enviar token:**
- Header: `Authorization: Bearer <token>`
- Query param: `?token=<token>`

El token se obtiene del endpoint `/login` en la respuesta:
```json
{
  "data": {
    "token": "eyJ..."
  },
  "status": "success",
  "message": "Login successful"
}
```

## Scripts Útiles

- `python seed.py` - Poblar base de datos con usuarios de prueba
- `python create_tables.py` - Crear tablas manualmente (si generate_schemas falla)
- `python check_postgres.py` - Verificar conexión a PostgreSQL

## Notas

- El modelo de ML debe estar en `model/model.keras`
- Las métricas y configuración del modelo en `model/metrics.json`
- En desarrollo, las cookies no usan `secure=True` (solo HTTP)
- El middleware JWT protege automáticamente todas las rutas excepto las públicas
