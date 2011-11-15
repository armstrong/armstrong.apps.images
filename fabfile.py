import os.path
from fabric.api import *
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
        'south',
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


@task
def update_colorbox():
    """Update Colorbox code from vendor tree"""
    base_name = os.path.dirname(__file__)
    destination = os.path.join(base_name, "armstrong", "apps", "images", "static", "colorbox")
    colorbox_source = os.path.join(base_name, "vendor", "colorbox")
    colorbox_files = [
        os.path.join(colorbox_source, "example1", "colorbox.css"),
        os.path.join(colorbox_source, "example1", "images"),
        os.path.join(colorbox_source, "colorbox", "jquery.colorbox-min.js"),
    ]
    local("cp -R %s %s" % (" ".join(colorbox_files), destination))

    # We're not supporting IE6, so we can drop the backfill
    local("rm -rf %s" % (os.path.join(destination, "images", "ie6")))
