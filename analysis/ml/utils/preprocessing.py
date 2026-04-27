import tensorflow as tf

IMG_SIZE = (256, 128)

def preprocess_image(file):
    img = tf.image.decode_png(file, channels=1)
    img = tf.image.resize(img, (128, 32))
    img = img / 255.0
    return img
