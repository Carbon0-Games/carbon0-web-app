from django.db import models
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

    def __str__(self):
        """Return a human-understandable name for the deep learning model."""
        return f"CNN with weights {self.weights}"

    def build(self):
        """Use the model fields to instantiate a neural network."""
        # Load Architecture
        with open(self.architecture, 'r') as f:
            model = keras.models.model_from_json(f.read())
            # Load Weights
            model.load_weights(self.weights)
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
        # preprocess the image data
        # predict on the image data
        # decide the status
        # decide the condition
        # add the confidence to the output
        # TODO: replace dummy output below
        return ["H", "No symptoms", 0.87]
