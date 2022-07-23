"""
WSGI config for config project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os
from dotenv import load_dotenv

from django.core.wsgi import get_wsgi_application

settings_module = os.environ.get("DJANGO_SETTINGS_MODULE")

if settings_module is None:
    settings_module = "config.local_settings"

os.environ.setdefault("DJANGO_SETTINGS_MODULE", settings_module)

if settings_module == "config.production_settings":
    project_folder = os.path.expanduser("~/rparse")
    load_dotenv(os.path.join(project_folder, ".env"))

application = get_wsgi_application()
