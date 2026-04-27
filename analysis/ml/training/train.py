from ..models.cnn_model import build_model
from ..utils.dataset import load_datasets, prepare
import tensorflow as tf

DATA_DIR = "analysis/ml/data/spiral"
MODEL_PATH = "ml_models/model.h5"

def train():
    train_ds, val_ds, _ = load_datasets(DATA_DIR)
    train_ds = prepare(train_ds)
    val_ds = prepare(val_ds)

    model = build_model()

    model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=20,
        callbacks=[
            tf.keras.callbacks.EarlyStopping(
                monitor='val_loss',
                patience=3,
                restore_best_weights=True
            ),
            tf.keras.callbacks.ModelCheckpoint(
                filepath=MODEL_PATH,
                monitor='val_loss',
                save_best_only=True
            )
        ]
    )

    # model.save(MODEL_PATH)
    print("Model zapisany!")

if __name__ == "__main__":
    train()
