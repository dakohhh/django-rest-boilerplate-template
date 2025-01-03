from .base import *  # noqa: F403
from config.env import env
import dj_database_url

DEBUG = env.bool('DJANGO_DEBUG', default=True)

ALLOWED_HOSTS = ["*"]

# Database
DATABASES = {
    "default": dj_database_url.parse(
        "postgresql://postgres:wisdom@localhost:5432/django-template", conn_max_age=600, conn_health_checks=True
    )
}

# EMAIL CONFIGURATION (DEVELOPMENT)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'localhost'
EMAIL_USE_TLS = False
EMAIL_PORT = 2525
EMAIL_HOST_USER = "user"
EMAIL_HOST_PASSWORD = "pass"
DEFAULT_FROM_EMAIL = "User <no-reply@django-rest-boiler-plate-template.com>"
