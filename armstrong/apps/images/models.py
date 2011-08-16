from armstrong.core.arm_content.mixins.images import ImageMixin
from armstrong.core.arm_content.mixins.images import SorlThumbnailMixin
from armstrong.apps.content.models import Content


class Image(Content, ImageMixin, SorlThumbnailMixin):
    pass
