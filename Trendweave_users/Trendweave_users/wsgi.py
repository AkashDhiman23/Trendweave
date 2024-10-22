"""
WSGI config for Trendweave_users project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application# type: ignore

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Trendweave_users.settings')

application = get_wsgi_application()
