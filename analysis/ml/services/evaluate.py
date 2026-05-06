import tensorflow as tf
import numpy as np
from sklearn.metrics import classification_report, confusion_matrix
import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

MODEL_PATH = "ml_models/model.h5"
TEST_DIR = "analysis/ml/data/spiral/testing" 
IMG_SIZE = (128, 128)
BATCH_SIZE = 32

def evaluate_model():
    print("⏳ Wczytywanie modelu...")
    model = tf.keras.models.load_model(MODEL_PATH)
    
    print(f"⏳ Pobieranie danych ze zbioru TESTOWEGO ({TEST_DIR})...")
    
    raw_test_ds = tf.keras.utils.image_dataset_from_directory(
        TEST_DIR,
        image_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        color_mode="grayscale",
        shuffle=False
    )
    
    class_names = raw_test_ds.class_names
    
    test_ds = raw_test_ds.map(lambda x, y: (x / 255.0, y))

    print(f"Wykryte klasy: {class_names}")
    print("🤖 Generowanie ostatecznego raportu...\n")
    
    y_true = np.concatenate([y for x, y in test_ds], axis=0)
    y_pred_probs = model.predict(test_ds, verbose=0)
    y_pred = (y_pred_probs > 0.5).astype(int)

    
    print("="*40)
    print("STATYSTYKI DLA ZBIORU TESTOWEGO")
    print("="*40)
    print(classification_report(y_true, y_pred, target_names=class_names))
    
    print("\nMACIERZ POMYŁEK:")
    cm = confusion_matrix(y_true, y_pred)
    print(f"Zdrowi rozpoznani jako Zdrowi: {cm[0][0]}")
    print(f"Zdrowi uznani za CHORYCH:      {cm[0][1]}")
    print(f"Chorzy uznani za ZDROWYCH:     {cm[1][0]}  <-- (Błąd krytyczny)")
    print(f"Chorzy rozpoznani jako Chorzy: {cm[1][1]}")
    print("="*40)

if __name__ == "__main__":
    evaluate_model()