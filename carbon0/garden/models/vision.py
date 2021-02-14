from django.db import models
import tensorflow.keras.models as keras_models


class Vision(models.Model):
    architecture = models.FileField(
        upload_to="neural_networks/architecture/",
        null=True, 
        help_text="JSON instructions for how to constrcut \
                  the underlying neural network."
    )
    weights = models.FileField(
        upload_to="neural_networks/parameters/",
        null=True, 
        help_text="Hadoop instructions for what weights and biases \
                  to give the underlying neural network."
    )
