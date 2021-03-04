import os
import sentry_sdk
from carbon0.settings.base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Configure the Sentry SDK (this way we can still get error logs)
sentry_sdk.init(
    dsn=str(os.getenv("SENTRY_DSN")),
    integrations=[DjangoIntegration()],
    traces_sample_rate=1.0,
    # associate users to errors
    send_default_pii=True,
)

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
