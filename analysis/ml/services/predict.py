import tensorflow as tf
from .load_model import get_model
from ml.utils.preprocessing import preprocess_image

MODEL_PATH = "ml_models/model.h5"

def predict(file_bytes):
    model = get_model(MODEL_PATH)

    img = preprocess_image(file_bytes)
    img = tf.expand_dims(img, axis=0)  # batch

    pred = model.predict(img)[0][0]

    return {
        "probability": float(pred),
        "label": "parkinson" if pred > 0.5 else "healthy"
    }
