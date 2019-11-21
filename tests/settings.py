import os
import sys
from unittest.mock import MagicMock

sys.modules["subscription.chargify"] = MagicMock()

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
INVOICES_PREFIX = "test"

ROOT_URLCONF = "tests.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": ["briefme_invoices/templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]
