import tensorflow_hub as hub
import tensorflow as tf
import tensorflow_text
import numpy as np
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
tf.config.list_physical_devices('GPU')


def get_bert_model():

    #get BERT Layers
    preprocess_url = 'https://tfhub.dev/tensorflow/bert_en_uncased_preprocess/3'
    encoder_url = 'https://tfhub.dev/tensorflow/bert_en_uncased_L-12_H-768_A-12/4'
    bert_preprocess_model = hub.KerasLayer(preprocess_url)
    bert_encoder = hub.KerasLayer(encoder_url)

    # BERT Layers
    text_input = tf.keras.layers.Input(shape=(), dtype=tf.string, name="text")
    preprocessed_text = bert_preprocess_model(text_input)
    outputs = bert_encoder(preprocessed_text)

    # Neural Network Layers
    network = tf.keras.layers.Dropout(0.1, name="dropout")(outputs['pooled_output'])
    network = tf.keras.layers.Dense(4, activation="softmax", name="output")(network)

    # Construct final Model
    bert_model = tf.keras.Model(inputs=[text_input], outputs=[network])

    # assign metrics
    METRICS = [
        tf.keras.metrics.Accuracy(name='accuracy'),
        tf.keras.metrics.Precision(name='precision'),
        tf.keras.metrics.AUC(name='auc')
    ]

    # compile the model
    bert_model.compile(
        optimizer='adam',
        loss='categorical_crossentropy',
        metrics=METRICS
    )
    return bert_model


def get_song_name_and_artist_emotion(txt: str) -> str:
    
    model = get_bert_model()
    input = []
    input.append(str)

    latest = tf.train.latest_checkpoint('./../models/song_bert_training_weights')
    if latest != None:
        model.load_weights(latest)

    pred = model.predict(input)
    emotion_number = np.argmax(pred)
    if emotion_number == 0:
        return 'happy'
    elif emotion_number == 1:
        return 'sad'
    elif emotion_number == 2:
        return 'angry'
    elif emotion_number == 3:
        return 'relaxed'


