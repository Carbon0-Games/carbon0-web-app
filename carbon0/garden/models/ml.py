from django.db import models
import tensorflow.keras.models as keras_models  # need to use model_from_json
from .leaf import Leaf


class MachineLearning(models.Model):
    PURPOSES = [
        ("V", "Computer Vision"),
        ("L", "Natural Language Processing"),
    ]
    purpose = models.CharField(
        max_length=1, help_text="Describe what the model does.",
        default="V", choices=PURPOSES
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
        """Uses the weights and architecture to instantiate a new CNN."""
        pass

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
        return ["H", "No symptoms", 0.87]

