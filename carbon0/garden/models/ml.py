import os
from pathlib import Path

import boto3
import botocore
from django.conf import settings
from django.db import models
import numpy as np
from PIL import Image
from tensorflow import keras
import tensorflow as tf

from .leaf import Leaf


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
    # save static files related to this model in app subdirectory
    # ARCH_UPLOAD_LOCATION = os.path.join(
    #     "garden", "neural_networks", "architecture"
    # )
    # WEIGHTS_UPLOAD_LOCATION = os.path.join(
    #     "garden", "neural_networks", "parameters"
    # )
    # architecture = models.FileField(
    #     upload_to=ARCH_UPLOAD_LOCATION,
    #     null=True,
    #     help_text="JSON instructions for how to constrcut \
    #               the underlying neural network.",
    # )
    # weights = models.FileField(
    #     upload_to=WEIGHTS_UPLOAD_LOCATION,
    #     null=True,
    #     help_text="Hadoop instructions for what weights and biases \
    #               to give the underlying neural network.",
    # )
    # Source: the "New Plant Diseases Dataset": https://tinyurl.com/dzav422a
    LEAF_LABELS = np.array([
        # entries MUST be formatted as "<species>_<condition>"
        'Strawberry_healthy',
        'Grape_Black rot',
        'Potato_Early blight',
        'Blueberry_healthy',
        'Corn_healthy',
        'Tomato_Target Spot',
        'Peach_healthy',
        'Potato_Late blight',
        'Tomato_Late blight',
        'Tomato_mosaic virus',
        'Bell pepper_healthy',
        'Orange_Haunglongbing (aka Citrus greening)',
        'Tomato_Leaf Mold',
        'Grape_Leaf blight (aka Isariopsis leaf spot)',
        'Cherry_Powdery mildew',
        'Apple_rust',
        'Tomato_Bacterial spot',
        'Grape_healthy',
        'Tomato_Early blight',
        'Corn_Common rust',
        'Grape_Black Measles',
        'Raspberry_healthy',
        'Tomato_healthy',
        'Cherry_healthy',
        'Tomato_Yellow Leaf Curl Virus',
        'Apple_scab',
        'Corn_Northern Leaf Blight',
        'Tomato_Two-spotted spider mite',
        'Peach_Bacterial spot',
        'Bell pepper_Bacterial spot',
        'Tomato_Septoria leaf spot',
        'Squash_Powdery mildew',
        'Corn_Gray leaf spot',
        'Apple_Black rot',
        'Apple_healthy',
        'Strawberry_Leaf scorch',
        'Potato_healthy',
        'Soybean_healthy'
    ])

    def __str__(self):
        """Return a human-understandable name for the deep learning model."""
        return f"CNN with weights {self.weights}"

    def build(self):
        """Use the model fields to instantiate a neural network."""
        # get the model files locally and from S#
        architecture_file_path = (
            "static/neural_networks/architecture/inceptionModelArchitecture.json"
        )
        params_file_path = (
            "static/neural_networks/parameters/inception_model_weights.h5"
        )
        # Load the Achitecture
        with open(architecture_file_path, 'r') as f:
            model = keras.models.model_from_json(f.read())
            # Load Weights
            model.load_weights(params_file_path)
            return model

    def diagnose(self, predictions):
        """Returns the model's label for a leaf image.

        Parameters:
        predictions(List[float]): a list of the probabilities 
        generated by the model for the image to belong is one of the classes

        Returns:
        List[str, float]: tells whether the model thinks the leaf is healthy;
        and if is unhealthy, it will also say what condition it has;
        and finally it will give the probability of the predicted class

        Notes:
        Our threshold for determining if the leaf is moderately healthy
        or not is between 8.33-10% confidence by the model. The justification
        for this is that we are only using the model to identify conditions
        on the leaves, not the actual species (that is handled by the user).

        Since there are only about 12 distinct conditions the leaf can be in
        (e.g. "healthy", "blight", "mold") in the labels listed above, we'll 
        use 1/12 as the lower end of our threshold. This is the minimum 
        confidence the model must have for one of the conditions above to 
        take majority. 
        
        The upper end of our threshold is set arbitrarily at
        10% - I'm not really sure if it's the best number, however since the
        model is not 100% accurate we know we at least need to have an
        upper threshold above 8.33%. This will prevent the model from
        labelling a plant healthy just without having at least some certainty.

        """
        LOWER_THRESHOLD = 0.83333
        UPPER_THRESHOLD = 0.10000
        # A: get the prediction label
        index_highest_proba = np.argmax(predictions)
        label = self.LEAF_LABELS[index_highest_proba]
        # B: get the prediction probability
        confidence = predictions[index_highest_proba]
        # C: init the status at "Moderate", one of the values in Leaf.STATUSES
        statuses = Leaf.get_status_abbreviations()
        status = statuses[0]
        # D: decide the condition
        condition = label.split("_")[-1]
        # E: change the status if necessary
        if confidence > UPPER_THRESHOLD:
            if condition == "healthy":
                status = statuses[1]  # stands for "Healthy"
            else:  # the model has confidence that the plant is not healthy
                status = statuses[2]
        return [status, condition, confidence]  

    def image_from_s3(self, img_url):
        """Returns an image stored as an object on AWS S3, as a Tensor.

        Parameter:
        img_url(str): an HTTPS address where the leaf image was saved on S3

        Returns: PIL.Image: representation of the image in Pillow  
        """ 
        # init AWS-relevant info
        s3 = boto3.resource('s3')
        bucket = s3.Bucket(settings.AWS_STORAGE_BUCKET_NAME)
        # get the path to the image on S3, leaving out the rest
        start_path = img_url.find("garden") 
        end_path = img_url.find("?")
        path = img_url[start_path:end_path]
        # get the image data, and convert to PIL.Image
        object = bucket.Object(path)
        response = object.get()
        return Image.open(response['Body']) 

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
        img_url = leaf.image.url  # URL in the cloud
        # if settings.DEBUG:  # TODO: make it work on a local filesystem path
        #     img_url =  (
        #         str(settings.BASE_DIR) + "/" 
        #         + Leaf.UPLOAD_LOCATION 
        #         + leaf.image.url
        #     )
        image = self.image_from_s3(img_url)
        tensor_image = keras.preprocessing.image.img_to_array(image)
        resized_img = tf.image.resize(tensor_image, [256, 256])
        final_image = tf.keras.applications.inception_v3.preprocess_input(resized_img)
        # make a 4D tensor before we're ready to predict
        final_input = np.expand_dims(final_image, axis=0)
        # predict on the image data - use an outer list to make a 4D Tensor
        prediction_probabilities = model(final_input, training=False)
        # return first array in output - these are predictions for that sample
        return self.diagnose(prediction_probabilities[0])
