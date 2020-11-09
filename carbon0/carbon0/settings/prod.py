from carbon0.settings.base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Mixpanel Project Token
MP_PROJECT_TOKEN = str(os.getenv("MP_PROJECT_TOKEN"))
