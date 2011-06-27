from django.conf import settings
from django.db import models
from sorl.thumbnail import ImageField
from armstrong.core.arm_content.mixins.images.sorl import SorlImageMixin
from armstrong.core.arm_content.mixins.authors import AuthorsMixin

UPLOAD_PATH = getattr(settings, 'ARMSTRONG_UPLOAD_PATH', 'armstrong/images/')

class Image(SorlImageMixin, AuthorsMixin):

    image = ImageField(upload_to=UPLOAD_PATH)
    title = models.CharField(max_length=100)
    caption = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return self.image.url

