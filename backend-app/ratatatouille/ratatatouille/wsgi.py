"""
WSGI config for ratatatouille project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

app_env = os.getenv('APP_ENV')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ratatatouille.settings.' + app_env)

application = get_wsgi_application()
