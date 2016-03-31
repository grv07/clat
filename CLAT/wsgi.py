"""
WSGI config for CLAT project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/howto/deployment/wsgi/
"""

import os
import sys

sys.path.append('/home/ubuntu/project/CLAT/')
sys.path.append('/home/ubuntu/project/env/lib/python2.7/site-packages/')

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CLAT.settings")

application = get_wsgi_application()
