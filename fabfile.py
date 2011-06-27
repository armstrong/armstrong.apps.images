import os.path
from armstrong.dev.tasks import *


settings = {
    'DEBUG': True,
    'INSTALLED_APPS': (
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.sites',
        'armstrong.core.arm_content',
        'armstrong.apps.images',
        'armstrong.apps.images.tests.images_support',
    ),
    'SITE_ID': 1,
    'ROOT_URLCONF': 'armstrong.apps.images.urls',
    'ARMSTRONG_UPLOAD_PATH': os.path.join(os.path.dirname(__file__),
            'test_uploads'),
}

pip_install_first = True
main_app = "images"
tested_apps = (main_app,)
