import tensorflow as tf
from tensorflow.keras.utils import image_dataset_from_directory

IMG_SIZE = (128, 32)
BATCH_SIZE = 32

"""
BASE_DIR = "data/augmented_hw_dataset"

train_ds = image_dataset_from_directory(f"{BASE_DIR}/training")
val_ds   = image_dataset_from_directory(f"{BASE_DIR}/validation")
test_ds  = image_dataset_from_directory(f"{BASE_DIR}/testing")
"""

def load_datasets(base_dir):
    train_ds = tf.keras.utils.image_dataset_from_directory(
        f"{base_dir}/training",
        image_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        color_mode="grayscale"
    )

    val_ds = tf.keras.utils.image_dataset_from_directory(
        f"{base_dir}/validation",
        image_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        color_mode="grayscale"
    )

    test_ds = tf.keras.utils.image_dataset_from_directory(
        f"{base_dir}/testing",
        image_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        color_mode="grayscale"
    )

    train_ds = train_ds.shuffle(1000)

    return train_ds, val_ds, test_ds


def prepare(ds):
    ds = ds.map(lambda x, y: (x / 255.0, y))
    ds = ds.cache().shuffle(1000).prefetch(tf.data.AUTOTUNE)
    return ds
