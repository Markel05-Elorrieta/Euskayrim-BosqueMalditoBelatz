import joblib
from pathlib import Path

from tensorflow import keras


class ModelLoader:
    _model = None
    _scaler = None

    @classmethod
    def load(cls) -> None:
        possible_dirs = [
            Path(__file__).resolve().parent.parent.parent.parent / "ad" / "models",
            Path.cwd(),
            Path(__file__).resolve().parent.parent,
        ]

        model_path = None
        scaler_path = None

        for directory in possible_dirs:
            candidate_model = directory / "ojo_del_oraculo.h5"
            candidate_scaler = directory / "scaler_oraculo.pkl"
            if candidate_model.exists() and candidate_scaler.exists():
                model_path = candidate_model
                scaler_path = candidate_scaler
                break

        if model_path and scaler_path:
            cls._model = keras.models.load_model(str(model_path))
            cls._scaler = joblib.load(scaler_path)
            print(f"Modelo y scaler cargados correctamente desde {model_path.parent}")
        else:
            cls._model = None
            cls._scaler = None
            print(
                "ERROR: No se encontró el modelo (.h5) y/o el scaler (.pkl)"
            )

    @classmethod
    def get_model(cls):
        return cls._model

    @classmethod
    def get_scaler(cls):
        return cls._scaler

    @classmethod
    def is_loaded(cls) -> bool:
        return cls._model is not None and cls._scaler is not None
