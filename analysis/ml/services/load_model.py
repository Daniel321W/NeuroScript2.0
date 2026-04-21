from tensorflow.keras.models import load_model

_model = None

def get_model(path):
    global _model
    if _model is None:
        _model = load_model(path)
    return _model
