import random
import os.path
import datetime
from django.test import TestCase as DjangoTestCase
from django.core.files import File
from ..models import Image

PATH_TO_IMG_FILE = os.path.join(os.path.dirname(__file__),
        'images_support/medellin.jpg')

def generate_random_image():
    title = 'Random title %s' % random.randint(100,1000)
    summary = 'Random summary %s' % random.randint(100,1000)
    f = open(PATH_TO_IMG_FILE)
    return Image.objects.create(title=title, summary=summary, image=File(f),
            pub_date=datetime.datetime.now())

class TestCase(DjangoTestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def assertInContext(self, var_name, other, template_or_context):
        # TODO: support passing in a straight "context" (i.e., dict)
        context = template_or_context.context_data
        self.assertTrue(var_name in context,
                msg="`%s` not in provided context" % var_name)
        self.assertEqual(context[var_name], other)
