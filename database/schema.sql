-- ============================================================
-- Schema de la base de datos de Euskayrim  (SQLite)
-- Generado como referencia; las tablas se crean con SQLAlchemy.
-- ============================================================

-- Héroes (los 6 Guardianes Ancestrales)
CREATE TABLE IF NOT EXISTS heroes (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre      VARCHAR(50)  NOT NULL UNIQUE,
    descripcion TEXT,
    vida        REAL NOT NULL DEFAULT 0.0,
    mana        REAL NOT NULL DEFAULT 0.0,
    fisico      REAL NOT NULL DEFAULT 0.0,
    agilidad    REAL NOT NULL DEFAULT 0.0,
);

-- Registro histórico de incursiones
CREATE TABLE IF NOT EXISTS incursiones (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    dificultad          REAL    NOT NULL,

    olenthero_en_equipo INTEGER DEFAULT 0,
    olenthero_vida      REAL    DEFAULT 0.0,
    olenthero_mana      REAL    DEFAULT 0.0,
    olenthero_fisico    REAL    DEFAULT 0.0,
    olenthero_agilidad  REAL    DEFAULT 0.0,

    thorgin_en_equipo   INTEGER DEFAULT 0,
    thorgin_vida        REAL    DEFAULT 0.0,
    thorgin_mana        REAL    DEFAULT 0.0,
    thorgin_fisico      REAL    DEFAULT 0.0,
    thorgin_agilidad    REAL    DEFAULT 0.0,

    amalyria_en_equipo  INTEGER DEFAULT 0,
    amalyria_vida       REAL    DEFAULT 0.0,
    amalyria_mana       REAL    DEFAULT 0.0,
    amalyria_fisico     REAL    DEFAULT 0.0,
    amalyria_agilidad   REAL    DEFAULT 0.0,

    basajorn_en_equipo  INTEGER DEFAULT 0,
    basajorn_vida       REAL    DEFAULT 0.0,
    basajorn_mana       REAL    DEFAULT 0.0,
    basajorn_fisico     REAL    DEFAULT 0.0,
    basajorn_agilidad   REAL    DEFAULT 0.0,

    lamyreth_en_equipo  INTEGER DEFAULT 0,
    lamyreth_vida       REAL    DEFAULT 0.0,
    lamyreth_mana       REAL    DEFAULT 0.0,
    lamyreth_fisico     REAL    DEFAULT 0.0,
    lamyreth_agilidad   REAL    DEFAULT 0.0,

    sugarth_en_equipo   INTEGER DEFAULT 0,
    sugarth_vida        REAL    DEFAULT 0.0,
    sugarth_mana        REAL    DEFAULT 0.0,
    sugarth_fisico      REAL    DEFAULT 0.0,
    sugarth_agilidad    REAL    DEFAULT 0.0,

    exito               INTEGER
);

-- Tabla asociativa héroes ↔ incursiones
CREATE TABLE IF NOT EXISTS incursion_heroes (
    id             INTEGER PRIMARY KEY AUTOINCREMENT,
    incursion_id INTEGER NOT NULL REFERENCES incursiones(id),
    heroe_id     INTEGER NOT NULL REFERENCES heroes(id),
    PRIMARY KEY (incursion_id, heroe_id)
);

-- Log de predicciones What-If3.
CREATE TABLE IF NOT EXISTS predicciones (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    dificultad          REAL    NOT NULL,

    olenthero_en_equipo INTEGER DEFAULT 0,
    thorgin_en_equipo   INTEGER DEFAULT 0,
    amalyria_en_equipo  INTEGER DEFAULT 0,
    basajorn_en_equipo  INTEGER DEFAULT 0,
    lamyreth_en_equipo  INTEGER DEFAULT 0,
    sugarth_en_equipo   INTEGER DEFAULT 0,

    probabilidad_exito  REAL    NOT NULL,
    prediccion          VARCHAR(20) NOT NULL
);
