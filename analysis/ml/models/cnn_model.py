from tensorflow.keras import layers, models
from tensorflow.keras import layers

data_augmentation = models.Sequential([
    layers.RandomRotation(0.02),
    layers.RandomZoom(0.1),
    layers.RandomTranslation(0.02, 0.02),
])

def build_model(input_shape=(128, 32, 1)):
    model = models.Sequential([
        layers.Input(shape=input_shape),
        data_augmentation,
        layers.Conv2D(32, (3,3), activation='relu'),
        layers.MaxPooling2D(),

        layers.Conv2D(64, (3,3), activation='relu'),
        layers.MaxPooling2D(),

        layers.Conv2D(128, (3,3), activation='relu'),
        layers.MaxPooling2D(),

        layers.Flatten(),
        layers.Dense(128, activation='relu'),
        layers.Dropout(0.5),

        layers.Dense(1, activation='sigmoid')
    ])

    model.compile(
        optimizer='adam',
        loss='binary_crossentropy',
        metrics=['accuracy', 'AUC']
    )

    return model
