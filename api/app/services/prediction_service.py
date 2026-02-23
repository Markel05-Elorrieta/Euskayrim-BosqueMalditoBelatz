import numpy as np
import pandas as pd
from fastapi import HTTPException

from api.app.ml.model_loader import ModelLoader
from api.app.ml.preprocessor import engineer_features
from api.app.schemas.incursion import Incursion


def predict_batch(incursions: list[Incursion]) -> list[dict]:
    """Versión batch de predict: procesa múltiples incursiones en una sola llamada al modelo."""
    model = ModelLoader.get_model()
    scaler = ModelLoader.get_scaler()

    if model is None or scaler is None:
        raise HTTPException(status_code=500, detail="El modelo no está cargado.")

    rows = [inc.model_dump() for inc in incursions]
    input_data = pd.DataFrame(rows)
    input_data = engineer_features(input_data)

    try:
        input_data = input_data[scaler.feature_names_in_]
    except KeyError as e:
        raise HTTPException(status_code=400, detail=f"Faltan columnas en los datos: {e}")

    input_scaled = scaler.transform(input_data)
    probas = model.predict(input_scaled, verbose=0).flatten()

    results = []
    for i, inc in enumerate(incursions):
        p = float(probas[i])
        results.append({
            "probabilidad_exito": round(p, 4),
            "prediccion": "Victoria" if p >= 0.5 else "Derrota",
            "dificultad_incursion": inc.dificultad,
        })
    return results


def predict(incursion: Incursion) -> dict:
    """Función que recibe los datos de una incursión, procesa los datos, y devuelve la predicción de éxito junto con la probabilidad"""
    model = ModelLoader.get_model()
    scaler = ModelLoader.get_scaler()

    if model is None or scaler is None:
        raise HTTPException(status_code=500, detail="El modelo no está cargado.")

    # Convertir los datos recibidos a un DataFrame
    input_data = pd.DataFrame([incursion.model_dump()])

    # Generar las variables  que el modelo espera
    input_data = engineer_features(input_data)

    # Asegurar que las columnas estén en el mismo orden que usó el scaler
    try:
        input_data = input_data[scaler.feature_names_in_]
    except KeyError as e:
        raise HTTPException(
            status_code=400,
            detail=f"Faltan columnas en los datos: {e}",
        )

    # Escalar los datos con el StandardScaler
    input_scaled = scaler.transform(input_data)

    # Predicción con la red neuronal
    prediction_proba = float(model.predict(input_scaled, verbose=0)[0][0])
    prediction_class = int(prediction_proba >= 0.5)

    return {
        "probabilidad_exito": round(prediction_proba, 4),
        "prediccion": "Victoria" if prediction_class == 1 else "Derrota",
        "dificultad_incursion": incursion.dificultad,
    }
