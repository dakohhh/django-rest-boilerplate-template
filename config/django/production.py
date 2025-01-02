from .base import *  # noqa: F403
import dj_database_url
from config.env import env



DEBUG = env.bool('DJANGO_DEBUG', default=False)

ALLOWED_HOSTS = env.list("ALLOWED_HOST", default=[])


DATABASES = {
    "default": dj_database_url.parse(
        "postgresql://postgres:wisdom@localhost:5432/django-template",
        conn_max_age=600,
        conn_health_checks=True,
    )
}

# EMAIL CONFIGURATION (PRODUCTION)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = env.str("MAILER_SMTP_HOST")
EMAIL_PORT = env.bool("MAILER_SMTP_PORT")
EMAIL_USE_TLS = env.bool("MAILER_SMTP_TLS")
EMAIL_HOST_USER = env.str("MAILER_SMTP_USER")
EMAIL_HOST_PASSWORD = env.str("MAILER_SMTP_PASSPORT")
DEFAULT_FROM_EMAIL = "User <no-reply@django-rest-boiler-plate-template.com>"



