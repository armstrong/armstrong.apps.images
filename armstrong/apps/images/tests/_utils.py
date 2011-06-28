import random, os.path
from django.test import TestCase as DjangoTestCase
from django.core.files import File
from ..models import Image

PATH_TO_IMG_FILE = os.path.join(os.path.dirname(__file__),
        'images_support/medellin.jpg')

def generate_random_image():
    title = 'Random title %s' % random.randint(100,1000)
    caption = 'Random caption %s' % random.randint(100,1000)
    f = open(PATH_TO_IMG_FILE)
    return Image.objects.create(title=title, caption=caption, image=File(f))

class TestCase(DjangoTestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def assertInContext(self, var_name, other, template_or_context):
        # TODO: support passing in a straight "context" (i.e., dict)
        context = template_or_context.context_data
        self.assertTrue(var_name in context,
                msg="`%s` not in provided context" % var_name)
        self.assertEqual(context[var_name], other)
