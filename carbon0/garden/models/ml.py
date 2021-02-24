from django.db import models
import numpy as np
from tensorflow import keras
import tensorflow as tf


class MachineLearning(models.Model):
    PURPOSES = [
        ("V", "Computer Vision"),
        ("L", "Natural Language Processing"),
    ]
    purpose = models.CharField(
        max_length=1,
        help_text="Describe what the model does.",
        default="V",
        choices=PURPOSES,
    )
    architecture = models.FileField(
        upload_to="neural_networks/architecture/",
        null=True,
        help_text="JSON instructions for how to constrcut \
                  the underlying neural network.",
    )
    weights = models.FileField(
        upload_to="neural_networks/parameters/",
        null=True,
        help_text="Hadoop instructions for what weights and biases \
                  to give the underlying neural network.",
    )
    # store a list of the classes the CNN model can label a leaf
    LEAF_LABELS = np.array([
        # labels were adapted from "New Plant Diseases Dataset": https://www.kaggle.com/vipoooool/new-plant-diseases-dataset
        'Strawberry___healthy',
        'Grape___Black_rot',
        'Potato___Early_blight',
        'Blueberry___healthy',
        'Corn_(maize)___healthy',
        'Tomato___Target_Spot',
        'Peach___healthy',
        'Potato___Late_blight',
        'Tomato___Late_blight',
        'Tomato___Tomato_mosaic_virus',
        'Pepper__bell___healthy',
        'Orange___Haunglongbing_(Citrus_greening)',
        'Tomato___Leaf_Mold',
        'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)',
        'Cherry_(including_sour)___Powdery_mildew',
        'Apple___Cedar_apple_rust',
        'Tomato___Bacterial_spot',
        'Grape___healthy',
        'Tomato___Early_blight',
        'Corn_(maize)___Common_rust_',
        'Grape___Esca_(Black_Measles)',
        'Raspberry___healthy',
        'Tomato___healthy',
        'Cherry_(including_sour)___healthy',
        'Tomato___Tomato_Yellow_Leaf_Curl_Virus',
        'Apple___Apple_scab',
        'Corn_(maize)___Northern_Leaf_Blight',
        'Tomato___Spider_mites Two-spotted_spider_mite',
        'Peach___Bacterial_spot',
        'Pepper,_bell___Bacterial_spot',
        'Tomato___Septoria_leaf_spot',
        'Squash___Powdery_mildew',
        'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot',
        'Apple___Black_rot',
        'Apple___healthy',
        'Strawberry___Leaf_scorch',
        'Potato___healthy',
        'Soybean___healthy'
    ])

    def __str__(self):
        """Return a human-understandable name for the deep learning model."""
        return f"CNN with weights {self.weights}"

    def build(self):
        """Use the model fields to instantiate a neural network."""
        # Load Architecture
        with open(self.architecture.url, 'r') as f:
            model = keras.models.model_from_json(f.read())
            # Load Weights
            model.load_weights(self.weights.url)
            return model

    def predict_health(self, leaf):
        """Predicts the status and condition of a Leaf, returns the confidence
        of the model as well.

        Parameter:
        leaf(Leaf): encapsulates the image to predict on

        Returns: List: structured as follows:
            - index 0: str: the status of the Leaf.
            - index 1: str: the symptoms found on the leaf
            - index 2: float: the percentage that the model thinks it's label
                       is correct.
        """
        # build the model
        model = self.build()
        # preprocess the image data
        img = tf.image.resize(leaf.image, [256, 256])
        final_image = tf.keras.applications.inception_v3.preprocess_input(img)
        # predict on the image data
        prediction_probabilities = model.predict(final_image)
        # TODO: decide the status, confidence, and condition
        confidence = np.argmax(prediction_probabilities)
        # TODO: replace dummy output below
        return ["H", "No symptoms", confidence]
