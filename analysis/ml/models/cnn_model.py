from tensorflow.keras import layers, models, optimizers

data_augmentation = models.Sequential([
    layers.RandomRotation(0.05),
    layers.RandomZoom(0.05),
])

def build_model(input_shape=(128, 128, 1)):
    model = models.Sequential([
        layers.Input(shape=input_shape),
        data_augmentation,
        
        layers.Conv2D(32, (3,3), padding='same'),
        layers.BatchNormalization(),
        layers.Activation('relu'),
        layers.MaxPooling2D(pool_size=(2,2)),

        layers.Conv2D(64, (3,3), padding='same'),
        layers.BatchNormalization(),
        layers.Activation('relu'),
        layers.MaxPooling2D(pool_size=(2,2)),

        layers.Conv2D(128, (3,3), padding='same'),
        layers.BatchNormalization(),
        layers.Activation('relu'),
        layers.MaxPooling2D(pool_size=(2,2)),

        layers.Flatten(),
        layers.Dense(128),
        layers.BatchNormalization(),
        layers.Activation('relu'),
        layers.Dropout(0.5),

        layers.Dense(1, activation='sigmoid')
    ])

    model.compile(
        optimizer=optimizers.Adam(learning_rate=0.001), 
        loss='binary_crossentropy',
        metrics=['accuracy', 'AUC']
    )

    return model