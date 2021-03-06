"""
Django settings for carbon0 project.

Generated by 'django-admin startproject' using Django 3.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
from django.conf import settings
from dotenv import load_dotenv
import django_heroku
import dj_database_url
import os
from pathlib import Path


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Loads in environment variables from a .env file
load_dotenv()

# The total number of "labels" that the AI model can make on a leaf
NUM_PREDICTION_LABELS = 38

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "accounts.apps.AccountsConfig",
    "carbon_quiz.apps.CarbonQuizConfig",
    "garden.apps.GardenConfig",
    "rest_framework",
    "storages",
    "social_django",  # Social Auth
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "social_django.middleware.SocialAuthExceptionMiddleware",  # Social Auth
]

ROOT_URLCONF = "carbon0.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],  # path to the project tempates
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                # Social Auth
                "social_django.context_processors.backends",
                "social_django.context_processors.login_redirect",
            ],
        },
    },
]

WSGI_APPLICATION = "carbon0.wsgi.application"

# Conversion Factors for Measurement Calculations in garden app
POUNDS_TO_KILOGRAMS = 0.45359237


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "carbon0",
        "USER": "postgres",
        "PASSWORD": str(os.getenv("DATABASE_PASSWORD")),
        "HOST": os.getenv("DB_HOST", "localhost"),
        "PORT": os.getenv("DB_PORT", "5432"),
    }
}

# Redirect back to login page on logout
LOGOUT_REDIRECT_URL = "accounts:login"

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

# Validator names
VAL_1 = "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
VAL_2 = "django.contrib.auth.password_validation.MinimumLengthValidator"
VAL_3 = "django.contrib.auth.password_validation.CommonPasswordValidator"
VAL_4 = "django.contrib.auth.password_validation.NumericPasswordValidator"

# Validators array
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": VAL_1},
    {"NAME": VAL_2},
    {"NAME": VAL_3},
    {"NAME": VAL_4},
]

# These are the levels a player can be at - used for scoring and
# recommendation algorithms
PLAYER_LEVELS = [
    (0, "Beginner Level"),
    (1, "Intermediate Level"),
    (2, "Advanced Level"),
    (3, "Expert Level"),
]

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = "en-us"

# Since we use PostgreSQL for the db, the time zone can be changed at any time;
# because the database takes care of converting datetimes to the desired time zone

TIME_ZONE = "America/New_York"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = "/static/"
# where to find static files in production
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# AWS S3 Variables
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID", "")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY", "")
AWS_STORAGE_BUCKET_NAME = os.getenv("AWS_STORAGE_BUCKET_NAME", "")

AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = None
DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"

# Facebook variables
FACEBOOK_SHARING_APP_ID = os.getenv("FACEBOOK_SHARING_APP_ID", "")

# Social Auth settings
SOCIAL_AUTH_URL_NAMESPACE = "social"

AUTHENTICATION_BACKENDS = (
    "social_core.backends.facebook.FacebookOAuth2",
    "social_core.backends.google.GoogleOAuth2",
    "django.contrib.auth.backends.ModelBackend",
)

LOGIN_URL = "accounts:login"
LOGOUT_URL = "logout"
LOGIN_REDIRECT_URL = "accounts:profile"

# SOCIAL_AUTH_LOGIN_ERROR_URL = '/settings/'
# SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/settings/'
# SOCIAL_AUTH_RAISE_EXCEPTIONS = False

SOCIAL_AUTH_FACEBOOK_KEY = os.getenv("SOCIAL_AUTH_FACEBOOK_KEY", "")
SOCIAL_AUTH_FACEBOOK_SECRET = os.getenv("SOCIAL_AUTH_FACEBOOK_SECRET", "")

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = os.getenv("SOCIAL_AUTH_GOOGLE_OAUTH2_KEY", "")
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = os.getenv("SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET", "")

SOCIAL_AUTH_FIELDS_STORED_IN_SESSION = ["secret_id"]

SOCIAL_AUTH_PIPELINE = (
    "social_core.pipeline.social_auth.social_details",
    "social_core.pipeline.social_auth.social_uid",
    "social_core.pipeline.social_auth.auth_allowed",
    "social_core.pipeline.social_auth.social_user",
    "social_core.pipeline.user.get_username",
    "social_core.pipeline.user.create_user",
    "accounts.views.create_social_user_with_achievement",  # set the path to the function
    "social_core.pipeline.social_auth.associate_user",
    "social_core.pipeline.social_auth.load_extra_data",
    "social_core.pipeline.user.user_details",
)

# Convert the DATABASE_URL environment variable into what Django understands
db_from_env = dj_database_url.config()
DATABASES["default"].update(db_from_env)

# Additional support setting up env for Heroku
django_heroku.settings(locals())
