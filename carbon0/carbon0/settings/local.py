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
DIET_ZERON_PATHS = [
    "assets/glb-files/carrot180.glb",
    "assets/usdz-files/carrot180.usdz",
]
TRANSIT_ZERON_PATHS = [
    "assets/glb-files/wheel180.glb",
    "assets/usdz-files/wheel180.usdz",
]
TREE_ZERON_PATHS = (
    [
        "assets/glb-files/tree.glb",
        "assets/usdz-files/tree.usdz",
    ],
)
RECYCLING_ZERON_PATHS = [
    "assets/glb-files/bin180.glb",
    "assets/usdz-files/bin180.usdz",
]
AT_ZERON_PATHS = [
    "assets/glb-files/coin180.glb",
    "assets/usdz-files/coin180.usdz",
]
UTIL_ZERON_PATHS = [
    "assets/glb-files/bulb180.glb",
    "assets/usdz-files/bulb180.usdz",
]
