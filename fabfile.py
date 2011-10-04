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
        'django.contrib.staticfiles',
        'armstrong.core.arm_access',
        'armstrong.core.arm_sections',
        'armstrong.apps.content',
        'armstrong.apps.images',
        'armstrong.apps.images.tests.support',
        'taggit',
        'sorl.thumbnail',
    ),
    'SITE_ID': 1,
    'ROOT_URLCONF': 'armstrong.apps.images.tests.support.urls',
    'ARMSTRONG_IMAGES_UPLOAD_PATH': 'uploads/',
    'MEDIA_ROOT': os.path.join(os.path.dirname(__file__),
                              'armstrong', 'apps', 'images',
                              'tests', 'support', 'media'),
    'MEDIA_URL': '/media/',
    'STATIC_URL': '/static/',
}

pip_install_first = True
main_app = "images"
tested_apps = (main_app,)
