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
RECYCLING_ZERON_PATHS = [
    str(os.getenv("RECYCLING_GLB")),
    str(os.getenv("RECYCLING_USDZ")),
]
AT_ZERON_PATHS = [str(os.getenv("AT_GLB")), str(os.getenv("AT_USDZ"))]
UTIL_ZERON_PATHS = [str(os.getenv("UTIL_GLB")), str(os.getenv("UTIL_USDZ"))]

# Mixpanel Project Token
MP_PROJECT_TOKEN = str(os.getenv("MP_PROJECT_TOKEN", ""))
