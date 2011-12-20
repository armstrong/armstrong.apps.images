from functools import wraps
import os.path
import PIL.Image
import shutil

from django.conf import settings
from django.core.urlresolvers import NoReverseMatch
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.test import TestCase

from armstrong.core.arm_sections.models import Section

from ._utils import generate_random_image, generate_random_imageset, \
                    LOCAL_IMAGE_PATH, SERVER_IMAGE_PATH
from ..models import Image


def skip_unless_app_urls_are_available(func):
    @wraps(func)
    def inner(self, *args, **kwargs):
        try:
            reverse("images_render_original", kwargs={"pk": 1})
            func(self, *args, **kwargs)
        except NoReverseMatch:
            self.skipTest("unable to load app-specific URLs")
    return inner


def skip_if_jpeg_decoder_not_available(func):
    @wraps(func)
    def inner(self, *args, **kwargs):
        if not hasattr(PIL.Image.core, "jpeg_decoder"):
            return self.skipTest("unable to load jpeg decoder for PIL")
        return func(self, *args, **kwargs)
    return inner


class ImageSetAdminTestCaseMixin:
    def setUp(self):
        self.image_sets = [generate_random_imageset() for i in range(5)]

    def test_browse_iset_without_search(self):
        response = self.client.get(reverse('admin:imagesets_admin_browse'))
        self.assertEqual(response.status_code, 200)
        for iset in self.image_sets:
            self.assertTrue(iset in response.context['imageset_list'])

    def test_browse_iset_unmatching_search(self):
        url = '%s?q=%s' % (reverse('admin:imagesets_admin_browse'), 'blahblah')
        response = self.client.get(url)
        self.assertEqual(len(response.context['imageset_list']), 0)

    def test_browse_iset_matching_search(self):
        self.image_sets[0].title = 'doodaaday'
        self.image_sets[0].save()

        url = '%s?q=%s' % (reverse('admin:imagesets_admin_browse'), 'doodaa')
        response = self.client.get(url)
        self.assertEqual(len(response.context['imageset_list']), 1)
        self.assertTrue(self.image_sets[0] in response.context['imageset_list'])

class ImageAdminTestCase(TestCase, ImageSetAdminTestCaseMixin):
    def setUp(self):
        user = User.objects.create_user('admin', 'admin@armstrongcms.org',
                                        'admin')
        user.is_superuser = True
        user.is_staff = True
        user.save()
        self.client.login(username='admin', password='admin')
        self.images = [generate_random_image() for i in range(10)]
        self.section = Section.objects.create(title='Test Section')

        ImageSetAdminTestCaseMixin.setUp(self)

    def tearDown(self):
        shutil.rmtree(os.path.join(settings.MEDIA_ROOT,
                                   settings.ARMSTRONG_IMAGES_UPLOAD_PATH))
        sorl_cache_path = os.path.join(settings.MEDIA_ROOT, 'cache')
        if os.path.isdir(sorl_cache_path):
            shutil.rmtree(sorl_cache_path)

    def test_browse_without_search(self):
        response = self.client.get(reverse('admin:images_admin_browse'))
        self.assertEqual(response.status_code, 200)
        for image in self.images:
            self.assertTrue(image in response.context['image_list'])

    def test_browse_unmatching_search(self):
        url = '%s?q=%s' % (reverse('admin:images_admin_browse'), 'blahblah')
        response = self.client.get(url)
        self.assertEqual(len(response.context['image_list']), 0)

    def test_browse_matching_search(self):
        self.images[0].title = 'doodaaday'
        self.images[0].save()

        url = '%s?q=%s' % (reverse('admin:images_admin_browse'), 'doodaa')
        response = self.client.get(url)
        self.assertEqual(len(response.context['image_list']), 1)
        self.assertTrue(self.images[0] in response.context['image_list'])

    def test_get_upload_form(self):
        response = self.client.get(reverse('admin:images_admin_upload'))
        self.assertEqual(response.status_code, 200)

    @skip_unless_app_urls_are_available
    def test_upload_image(self):
        self.assertTrue(not Image.objects.filter(title='uploaded').exists())
        f = open(LOCAL_IMAGE_PATH)
        url = reverse('admin:images_admin_upload')
        response = self.client.post(url, {
                'image': f,
                'title': 'uploaded',
                'slug': 'uploaded',
                'summary': 'uploaded image',
                'authors_override': 'bob marley',
                'pub_date': '2011-08-15',
                'pub_status': 'D',
                'tags': 'test tags',
                'access_is_public': '1',
                'primary_section': self.section.id,
                'sites': Site.objects.get_current().id,
                }, follow=True)
        f.close()
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Image.objects.filter(title='uploaded').exists())
        self.assertTrue(os.path.exists(SERVER_IMAGE_PATH))

    @skip_unless_app_urls_are_available
    @skip_if_jpeg_decoder_not_available
    def test_render_thumbnail(self):
        url = reverse('images_render_thumbnail',
                kwargs={'pk': self.images[0].id, 'geometry': '100x200'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    @skip_unless_app_urls_are_available
    def test_render_original(self):
        url = reverse('images_render_original',
                      kwargs={'pk': self.images[0].id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.images[0].image.url in response['location'])
