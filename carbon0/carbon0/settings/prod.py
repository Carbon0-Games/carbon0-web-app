import os
from carbon0.settings.base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = str(os.getenv("SECRET_KEY"))

ALLOWED_HOSTS = ["carbon0.herokuapp.com", "playcarbon0.com"]

# File paths for the Zeron model files
DIET_ZERON_PATHS = [str(os.getenv("DIET_GLB")), str(os.getenv("DIET_USDZ"))]
TRANSIT_ZERON_PATHS = [str(os.getenv("TRANSIT_GLB")), str(os.getenv("TRANSIT_USDZ"))]
TREE_ZERON_PATHS = [str(os.getenv("TREE_GLB")), str(os.getenv("TREE_USDZ"))]
RECYCLING_ZERON_PATHS = [
    str(os.getenv("RECYCLING_GLB")),
    str(os.getenv("RECYCLING_USDZ")),
]
AT_ZERON_PATHS = [str(os.getenv("AT_GLB")), str(os.getenv("AT_USDZ"))]
UTIL_ZERON_PATHS = [str(os.getenv("UTIL_GLB")), str(os.getenv("UTIL_USDZ"))]

# Mixpanel Project Token
MP_PROJECT_TOKEN = str(os.getenv("MP_PROJECT_TOKEN", ""))

# AWS S3 Variables
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID", "")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY", "")
AWS_STORAGE_BUCKET_NAME = os.getenv("AWS_STORAGE_BUCKET_NAME", "")

AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = None
DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
