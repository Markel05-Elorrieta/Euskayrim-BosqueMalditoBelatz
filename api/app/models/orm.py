"""Modelos ORM de SQLAlchemy para Euskayrim."""

from datetime import datetime, timezone

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Table,
    Text,
)
from sqlalchemy.orm import relationship

from api.app.database import Base

# Relación incursión - héroes
incursion_heroes = Table(
    "incursion_heroes",
    Base.metadata,
    Column("incursion_id", Integer, ForeignKey("incursiones.id"), primary_key=True),
    Column("heroe_id", Integer, ForeignKey("heroes.id"), primary_key=True),
)


# Héroes
class HeroeDB(Base):
    __tablename__ = "heroes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(50), unique=True, nullable=False, index=True)
    descripcion = Column(Text, nullable=True)

    # Stats base
    vida = Column(Float, nullable=False, default=0.0)
    mana = Column(Float, nullable=False, default=0.0)
    fisico = Column(Float, nullable=False, default=0.0)
    agilidad = Column(Float, nullable=False, default=0.0)

    # Relaciones
    incursiones = relationship(
        "IncursionDB", secondary=incursion_heroes, back_populates="heroes"
    )

    def __repr__(self):
        return f"<HeroeDB(id={self.id}, nombre='{self.nombre}')>"


# Incursión  ─  registro histórico de una partida
class IncursionDB(Base):
    __tablename__ = "incursiones"

    id = Column(Integer, primary_key=True, autoincrement=True)
    dificultad = Column(Float, nullable=False)

    # Stats por héroe en esta incursión concreta
    olenthero_en_equipo = Column(Integer, default=0)
    olenthero_vida = Column(Float, default=0.0)
    olenthero_mana = Column(Float, default=0.0)
    olenthero_fisico = Column(Float, default=0.0)
    olenthero_agilidad = Column(Float, default=0.0)

    thorgin_en_equipo = Column(Integer, default=0)
    thorgin_vida = Column(Float, default=0.0)
    thorgin_mana = Column(Float, default=0.0)
    thorgin_fisico = Column(Float, default=0.0)
    thorgin_agilidad = Column(Float, default=0.0)

    amalyria_en_equipo = Column(Integer, default=0)
    amalyria_vida = Column(Float, default=0.0)
    amalyria_mana = Column(Float, default=0.0)
    amalyria_fisico = Column(Float, default=0.0)
    amalyria_agilidad = Column(Float, default=0.0)

    basajorn_en_equipo = Column(Integer, default=0)
    basajorn_vida = Column(Float, default=0.0)
    basajorn_mana = Column(Float, default=0.0)
    basajorn_fisico = Column(Float, default=0.0)
    basajorn_agilidad = Column(Float, default=0.0)

    lamyreth_en_equipo = Column(Integer, default=0)
    lamyreth_vida = Column(Float, default=0.0)
    lamyreth_mana = Column(Float, default=0.0)
    lamyreth_fisico = Column(Float, default=0.0)
    lamyreth_agilidad = Column(Float, default=0.0)

    sugarth_en_equipo = Column(Integer, default=0)
    sugarth_vida = Column(Float, default=0.0)
    sugarth_mana = Column(Float, default=0.0)
    sugarth_fisico = Column(Float, default=0.0)
    sugarth_agilidad = Column(Float, default=0.0)

    exito = Column(Integer, nullable=True)

    # Relaciones
    heroes = relationship(
        "HeroeDB", secondary=incursion_heroes, back_populates="incursiones"
    )

    def __repr__(self):
        return (
            f"<IncursionDB(id={self.id}, "
            f"dificultad={self.dificultad}, exito={self.exito})>"
        )


# Predicción
class PrediccionDB(Base):
    __tablename__ = "predicciones"

    id = Column(Integer, primary_key=True, autoincrement=True)

    dificultad = Column(Float, nullable=False, default=0.0)

    # Composición del equipo enviado
    olenthero_en_equipo = Column(Integer, default=0)
    thorgin_en_equipo = Column(Integer, default=0)
    amalyria_en_equipo = Column(Integer, default=0)
    basajorn_en_equipo = Column(Integer, default=0)
    lamyreth_en_equipo = Column(Integer, default=0)
    sugarth_en_equipo = Column(Integer, default=0)

    # Resultado de la predicción
    probabilidad_exito = Column(Float, nullable=False)
    prediccion = Column(String(20), nullable=False)

    def __repr__(self):
        return (
            f"<PrediccionDB(id={self.id}, prob={self.probabilidad_exito}, "
            f"pred='{self.prediccion}')>"
        )
