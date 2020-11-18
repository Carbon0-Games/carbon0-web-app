import os
from carbon0.settings.base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Mixpanel Project Token
MP_PROJECT_TOKEN = ""

SECRET_KEY = "84#be86m-0ud#g$m&#6^)hd!$qyhl6mw73nm11$)=jufb-cw+4"

ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
]

# File paths for the Zeron model files
DIET_ZERON_PATHS = [str(os.getenv("DIET_GLB")), str(os.getenv("DIET_USDZ"))]
TRANSIT_ZERON_PATHS = [str(os.getenv("TRANSIT_GLB")), str(os.getenv("TRANSIT_USDZ"))]
RECYCLING_ZERON_PATHS = [
    str(os.getenv("RECYCLING_GLB")),
    str(os.getenv("RECYCLING_USDZ")),
]
AT_ZERON_PATHS = [str(os.getenv("AT_GLB")), str(os.getenv("AT_USDZ"))]
UTIL_ZERON_PATHS = [str(os.getenv("UTIL_GLB")), str(os.getenv("UTIL_USDZ"))]
