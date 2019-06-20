"""
WSGI config for huaxh_web project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

profile = os.environ.get('HUAXH_WEB_PROFILE','develop')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'huaxh_web.settings.%s' % profile)

application = get_wsgi_application()
