import random
import os.path
import datetime

from django.conf import settings
from django.core.files import File
from django.test import TestCase as DjangoTestCase

from ..models import Image


LOCAL_IMAGE_PATH = os.path.join(os.path.dirname(__file__),
                                'support', 'medellin.jpg')
SERVER_IMAGE_PATH = os.path.join(settings.MEDIA_ROOT,
                                 settings.ARMSTRONG_IMAGES_UPLOAD_PATH,
                                'medellin.jpg')

def generate_random_image():
    title = 'Random title %s' % random.randint(100, 1000)
    summary = 'Random summary %s' % random.randint(100, 1000)
    pub_date = datetime.datetime.now()
    f = open(LOCAL_IMAGE_PATH)
    with open(LOCAL_IMAGE_PATH) as f:
        im = Image.objects.create(title=title, summary=summary,
                                  pub_date=pub_date, image=File(f))
    return im


class TestCase(DjangoTestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def assertInContext(self, var_name, other, template_or_context):
        # TODO: support passing in a straight "context" (i.e., dict)
        context = template_or_context.context_data
        self.assertTrue(var_name in context,
                msg="`%s` not in provided context" % var_name)
        self.assertEqual(context[var_name], other)
