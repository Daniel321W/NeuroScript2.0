import tensorflow as tf

IMG_SIZE = (128, 32)
BATCH_SIZE = 32

def load_datasets(data_dir):
    train_ds = tf.keras.utils.image_dataset_from_directory(
        data_dir,
        validation_split=0.2,
        subset="training",
        seed=42,
        image_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        color_mode="grayscale"
    )

    val_ds = tf.keras.utils.image_dataset_from_directory(
        data_dir,
        validation_split=0.2,
        subset="validation",
        seed=42,
        image_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        color_mode="grayscale"
    )

    return train_ds, val_ds


def prepare(ds):
    ds = ds.map(lambda x, y: (x / 255.0, y))
    ds = ds.cache().shuffle(1000).prefetch(buffer_size=tf.data.AUTOTUNE)
    return ds
