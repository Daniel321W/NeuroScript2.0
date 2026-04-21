from ml.models.cnn_model import build_model
from ml.utils.dataset import load_datasets, prepare

DATA_DIR = "data/train"
MODEL_PATH = "ml_models/model.h5"

def train():
    train_ds, val_ds = load_datasets(DATA_DIR)
    print(train_ds.class_names)
    train_ds = prepare(train_ds)
    val_ds = prepare(val_ds)

    model = build_model()

    model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=20
    )

    model.save(MODEL_PATH)
    print("Model zapisany!")

if __name__ == "__main__":
    train()
