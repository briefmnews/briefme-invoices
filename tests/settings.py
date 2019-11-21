import os
import sys
from unittest.mock import MagicMock

sys.modules['subscription.chargify'] = MagicMock()

SECRET_KEY = "dump-secret-key"

INSTALLED_APPS = (
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.admin",
    "briefme_invoices",
    "briefme_test_user",
)

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "test",
        "USER": "briefme",
        "PASSWORD": "briefme",
        "HOST": "localhost",
    }
}

AUTH_USER_MODEL = "briefme_test_user.User"

INVOICES_PDF_ATTACHMENT = True

ROOT_URLCONF = "briefme_invoices.urls"
