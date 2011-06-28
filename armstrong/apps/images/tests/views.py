import os.path
from django.test.client import Client
from django.core.urlresolvers import reverse
from ._utils import generate_random_image, TestCase
from ..models import Image


class BrowseImagesTestCase(TestCase):
    
    def setUp(self):

        self.c = Client()
        self.images = [generate_random_image() for i in range(10)]    

    def test_browse_without_search(self):

        response = self.c.get(reverse('images_admin_browse'))

        for image in self.images:
            self.assertTrue(image in response.context['image_list'])

    def test_browse_unmatching_search(self):

        url = '%s?q=%s' % (reverse('images_admin_browse'), 'blahblah')
        response = self.c.get(url)
        self.assertEqual(len(response.context['image_list']), 0)

    def test_browse_matching_search(self):

        self.images[0].title = 'doodaaday'
        self.images[0].save()

        url = '%s?q=%s' % (reverse('images_admin_browse'), 'doodaa')
        response = self.c.get(url)
        self.assertEqual(len(response.context['image_list']), 1)
        self.assertTrue(self.images[0] in response.context['image_list'])

    def test_upload_image(self):

        f = open(os.path.join(os.path.dirname(__file__),
                'images_support/medellin.jpg'))

        data = {
            'image': f,
            'title': 'uploaded img',
            'authors_override': 'bob marley',
        }

        response = self.c.post(reverse('images_admin_upload'), data, 
                follow=True)
        f.close()

        self.assertTrue(Image.objects.filter(title=data['title']).exists())
