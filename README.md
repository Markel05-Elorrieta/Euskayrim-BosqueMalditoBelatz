# Euskayrim — Reto Final (Markel & Arian)

Frontend (HTML, CSS y JS) + API + modelo de Machine Learning para predecir el éxito de incursiones en el **Bosque Maldito de Belatz** de Euskayrim, donde los 6 héroes luchan contra las fuerzas oscuras.

## Inicio rápido

```bash
# 1. Instalar dependencias necesarias en el proyecto
pip install -r requirements.txt

# 2. Poblar la base de datos con datos históricos
python -m database.populate_db

# 3. Arrancar la API
python run_api.py
```

La API estará disponible en `http://localhost:8000` y la documentación Swagger UI en `/docs`.

Con la API iniciada, puedes acceder al frontend en `http://localhost:8000/static`.

---

## Estructura del proyecto

```
├── ad/                  # Análisis de datos
│   ├── data/            #   CSVs (crudo y limpio)
│   ├── models/          #   Modelo de red neuronal
│   └── notebooks/       #   Notebooks de exploración y entrenamiento
├── api/                 # API REST -> FastAPI
│   ├── app/
│   │   ├── main.py          # Punto de entrada de la app
│   │   ├── database.py      # Configuración SQLAlchemy
│   │   ├── ml/              # Carga del modelo y preprocesado
│   │   ├── models/          # ORM y dominio
│   │   ├── routers/         # Endpoints (health, heroes, what-if, divine-call)
│   │   ├── schemas/         # Esquemas Pydantic
│   │   └── services/        # Lógica
│   ├── static/              # Frontend (HTML/CSS/JS)
│   └── tests/               # Tests
├── database/            # Scripts de inicialización y carga
│   ├── init_db.py
│   ├── populate_db.py
│   └── schema.sql
├── docs/                # Informe
├── run_api.py           # Iniciador de la API con Uvicorn
└── requirements.txt
```

---

## Esquema de la base de datos

La aplicación utiliza **SQLite** gestionado con **SQLAlchemy ORM**. Las tablas se crean automáticamente al arrancar la API (`Base.metadata.create_all`). A continuación se describe cada tabla y sus relaciones:

### Diagrama entidad-relación

```
┌──────────────┐        ┌─────────────────────┐        ┌───────────────┐
│    heroes    │        │  incursion_heroes   │        │  incursiones  │
├──────────────┤        │     (N:M)           │        ├───────────────┤
│ PK id        │◄───────┤ PK,FK heroe_id      │        │ PK id         │
│    nombre    │        │ PK,FK incursion_id  ├───────►│    dificultad │
│    descr     │        └─────────────────────┘        │    *_en_equipo│
│    vida      │                                       │    *_vida     │
│    mana      │                                       │    *_mana     │
│    fisico    │                                       │    *_fisico   │
│    agilidad  │                                       │    *_agilidad │
└──────────────┘                                       │    exito      │
                                                       └───────────────┘

                        ┌──────────────────────┐
                        │    predicciones      │
                        ├──────────────────────┤
                        │ PK id                │
                        │    dificultad        │
                        │    *_en_equipo (×6)  │
                        │    probabilidad_exito│
                        │    prediccion        │
                        └──────────────────────┘
```

### Tabla `heroes`

Almacena los **6 Guardianes Ancestrales** del mundo de Euskayrim.

| Columna       | Tipo          | Restricciones              | Descripción                            |
|---------------|---------------|----------------------------|----------------------------------------|
| `id`          | `INTEGER`     | PK, autoincrement          | Identificador único del héroe          |
| `nombre`      | `VARCHAR(50)` | NOT NULL, UNIQUE, INDEX    | Nombre del guardián                    |
| `descripcion` | `TEXT`        | nullable                   | Descripción o trasfondo del héroe      |
| `vida`        | `REAL`        | NOT NULL, default 0.0      | Puntos de vida base                    |
| `mana`        | `REAL`        | NOT NULL, default 0.0      | Puntos de maná base                    |
| `fisico`      | `REAL`        | NOT NULL, default 0.0      | Estadística de fuerza física base      |
| `agilidad`    | `REAL`        | NOT NULL, default 0.0      | Estadística de agilidad base           |

**Héroes disponibles:** Olenthero, Thorgin, Amalyria, Basajörn, Lamyreth, Sugarth.

---

### Tabla `incursiones`

Registro histórico de cada partida/incursión al Bosque Maldito. Cada fila desnormaliza las estadísticas de los 6 héroes para facilitar la alimentación directa al modelo de ML.

| Columna                | Tipo      | Restricciones         | Descripción                                       |
|------------------------|-----------|-----------------------|---------------------------------------------------|
| `id`                   | `INTEGER` | PK, autoincrement     | Identificador único de la incursión               |
| `dificultad`           | `REAL`    | NOT NULL              | Nivel de dificultad de la incursión               |
| `<heroe>_en_equipo`    | `INTEGER` | default 0             | 1 si el héroe participó, 0 en caso contrario      |
| `<heroe>_vida`         | `REAL`    | default 0.0           | Vida del héroe en esta incursión concreta          |
| `<heroe>_mana`         | `REAL`    | default 0.0           | Maná del héroe en esta incursión                   |
| `<heroe>_fisico`       | `REAL`    | default 0.0           | Físico del héroe en esta incursión                 |
| `<heroe>_agilidad`     | `REAL`    | default 0.0           | Agilidad del héroe en esta incursión               |
| `exito`                | `INTEGER` | nullable              | Resultado: 1 = éxito, 0 = fracaso                 |

> `<heroe>` se repite para cada uno de los 6 héroes: `olenthero`, `thorgin`, `amalyria`, `basajorn`, `lamyreth`, `sugarth` (5 columnas × 6 héroes = **30 columnas de stats** + `dificultad` + `exito`).

---

### Tabla `incursion_heroes`

Tabla asociativa **N:M** que vincula qué héroes participaron en cada incursión.

| Columna        | Tipo      | Restricciones                        | Descripción                        |
|----------------|-----------|--------------------------------------|------------------------------------|
| `incursion_id` | `INTEGER` | PK, FK → `incursiones.id`            | Referencia a la incursión          |
| `heroe_id`     | `INTEGER` | PK, FK → `heroes.id`                 | Referencia al héroe participante   |

Cada incursión tiene exactamente **4 héroes** en el equipo.

---

### Tabla `predicciones`

Log de consultas **What-If** al Oráculo (modelo de red neuronal). Registra la composición del equipo propuesta y la predicción obtenida.

| Columna                | Tipo          | Restricciones         | Descripción                                            |
|------------------------|---------------|-----------------------|--------------------------------------------------------|
| `id`                   | `INTEGER`     | PK, autoincrement     | Identificador único de la predicción                   |
| `dificultad`           | `REAL`        | NOT NULL, default 0.0 | Nivel de dificultad consultado                         |
| `olenthero_en_equipo`  | `INTEGER`     | default 0             | 1 si Olenthero forma parte del equipo propuesto        |
| `thorgin_en_equipo`    | `INTEGER`     | default 0             | 1 si Thorgin forma parte del equipo propuesto          |
| `amalyria_en_equipo`   | `INTEGER`     | default 0             | 1 si Amalyria forma parte del equipo propuesto         |
| `basajorn_en_equipo`   | `INTEGER`     | default 0             | 1 si Basajörn forma parte del equipo propuesto         |
| `lamyreth_en_equipo`   | `INTEGER`     | default 0             | 1 si Lamyreth forma parte del equipo propuesto         |
| `sugarth_en_equipo`    | `INTEGER`     | default 0             | 1 si Sugarth forma parte del equipo propuesto          |
| `probabilidad_exito`   | `REAL`        | NOT NULL              | Probabilidad de éxito devuelta por el modelo (0.0–1.0) |
| `prediccion`           | `VARCHAR(20)` | NOT NULL              | Etiqueta de la predicción (e.g. "Éxito" / "Fracaso")   |

---

### Relaciones

- **heroes ↔ incursiones** — Relación N-M a través de `incursion_heroes`. Un héroe puede participar en múltiples incursiones y cada incursión tiene 4 héroes.
- **predicciones** — Tabla independiente (sin FKs). Actúa como log de auditoría de las predicciones del modelo What-If.

---

## Modelo de dominio

El código también define clases de dominio puro (sin ORM) en `api/app/models/domain.py`:

- **`Heroe`** — Clase base con stats (`vida`, `mana`, `fisico`, `agilidad`). Subclases: `Olenthero`, `Thorgin`, `Amalyria`, `Basajorn`, `Lamyreth`, `Sugarth`.
- **`BendicionIlargi`** — Distribución de 5 puntos de bonificación entre las 4 stats.
- **`Equipo`** — 4 héroes + 1 bendición. Valida que no haya duplicados y que la bendición sume 5.
- **`Incursion`** — Resultado de una partida (equipo + éxito/fracaso).

---

## Endpoints principales

| Método   | Ruta             | Descripción                                      |
|----------|------------------|--------------------------------------------------|
| GET      | `/`              | Mensaje de bienvenida                            |
| GET      | `/health`        | Estado de la API                                 |
| GET      | `/heroes`        | GET de todos los héroes                          |
| POST     | `/what-if`       | Predicción What-If con el modelo de red neuronal |
| POST     | `/divine-call`   | Devuelve la mejor combinación de héroes y bendición óptima por dificultad |

### Cómo funcionan los endpoints de predicción

#### `POST /what-if`

- **Qué hace:** evalúa una incursión concreta y estima su probabilidad de éxito.
- **Entrada:** un objeto `Incursion` con `dificultad` y las variables de equipo/stats de los 6 héroes (`*_en_equipo`, `*_vida`, `*_mana`, `*_fisico`, `*_agilidad`).
- **Salida:** JSON con `probabilidad_exito` (float entre 0 y 1) y `prediccion` (etiqueta de éxito/fracaso).

#### `POST /divine-call`

- **Qué hace:** busca la mejor combinación de 4 héroes y la bendición óptima para maximizar el éxito.
- **Entrada:** `{ "dificultad": 1|2|3 }`.
- **Salida:** `heroes`, `probabilidad_maxima`, `prediccion`, `dificultad`, `bendicion_optima` y `todas_combinaciones` (ordenadas por probabilidad).

Documentación interactiva disponible en `/docs` (Swagger UI)