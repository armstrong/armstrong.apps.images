import os.path
import datetime
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from ._utils import generate_random_image, TestCase
from ..models import Image


class BrowseImagesTestCase(TestCase):
    
    def setUp(self):

        user = User.objects.create_user('admin', 'admin@armstrongcms.org',
                'admin')
        user.is_superuser = True
        user.is_staff = True
        user.save()

        self.c = Client()
        self.c.login(username='admin', password='admin')

        self.images = [generate_random_image() for i in range(10)]    

    def test_browse_without_search(self):

        response = self.c.get(reverse('admin:images_admin_browse'))

        for image in self.images:
            self.assertTrue(image in response.context['image_list'])

    def test_browse_unmatching_search(self):

        url = '%s?q=%s' % (reverse('admin:images_admin_browse'), 'blahblah')
        response = self.c.get(url)
        self.assertEqual(len(response.context['image_list']), 0)

    def test_browse_matching_search(self):

        self.images[0].title = 'doodaaday'
        self.images[0].save()

        url = '%s?q=%s' % (reverse('admin:images_admin_browse'), 'doodaa')
        response = self.c.get(url)
        self.assertEqual(len(response.context['image_list']), 1)
        self.assertTrue(self.images[0] in response.context['image_list'])

    def test_get_upload_form(self):

        response = self.c.get(reverse('admin:images_admin_upload'))
        self.assertEqual(response.status_code, 200)

    def test_render_thumbnail(self):

        url = reverse('images_render_thumbnail',
                kwargs={'pk': self.images[0].id, 'geometry': '100x200'})

        response = self.c.get(url)

        self.assertEqual(response.status_code, 302)

    def test_render_original(self):

        url = reverse('images_render_original',
                kwargs={'pk': self.images[0].id})

        response = self.c.get(url)

        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.images[0].image.url in response['location'])
