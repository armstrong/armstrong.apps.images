from django.db import models

from armstrong.core.arm_content.mixins.images import ImageMixin
from armstrong.core.arm_content.mixins.images import SorlThumbnailMixin
from armstrong.apps.content.models import Content

class Image(Content, ImageMixin, SorlThumbnailMixin):
    pass

class ImageSet(Content):
    def first_element(self):
        if self.imagesetelement_set.all().count() > 0:
            return self.imagesetelement_set.all()[0]
            
        return None
        
class ImageSetElement(models.Model):
    image = models.ForeignKey(Image)
    imageset = models.ForeignKey(ImageSet)
    caption = models.CharField(blank=True, null=True, max_length=255)
    order = models.IntegerField()
    
    def __unicode__ (self):
        return '%d - %s' % (self.order, self.caption[:35])
        
    class Meta:
        ordering = ('order',)
        