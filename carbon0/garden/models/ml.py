import json
import requests

import boto3
from django.conf import settings
from django.db import models

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

    def __str__(self):
        """Return a human-understandable name for the deep learning model."""
        return f"CNN {self.id}"

    def get_prediction(self, image):
        # A: convert the image saved in the cloud into a bytes-like object
        img_data = image.read()
        img_bytes = bytearray(img_data)
        files = {'image': img_bytes}
        # B: get the predcitions from the Plant Vision API
        url = "https://plantvision.herokuapp.com/Diagnosis/prediction"
        response = requests.post(url, files=files)
        # C: parse the response 
        label, confidence = (
            json.loads(response.text)['label'],
            json.loads(response.text)['confidence'],
        )
        return [label, confidence]

    def diagnose(self, prediction):
        """Returns the model's label for a leaf image.

        Parameters:
        prediction(List[str, float]): the label and confidence 
            that the Plant Vision API gave to our user's leaf image

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
        # A: get the prediction label and confidence
        label, confidence = prediction
        # C: init the status at "Moderate", one of the values in Leaf.STATUSES
        statuses = Leaf.get_status_abbreviations()
        status = statuses[0]
        # D: decide the condition (last part of the label string)
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
        # return Image.open(response['Body']) 
        return response['Body']

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
        # get the image data
        img_url = leaf.image.url  # URL in the cloud
        image = self.image_from_s3(img_url)
        # predict on the image data - use the Plant Vision API
        prediction = self.get_prediction(image)
        # process the predictions
        return self.diagnose(prediction)
