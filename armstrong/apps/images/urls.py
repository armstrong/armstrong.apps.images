from django.conf.urls.defaults import *
from django.contrib.auth.decorators import permission_required

from .models import Image
from .views import RenderThumbnail


urlpatterns = patterns('',
    url(r'^thumbnail/(?P<pk>\d+)/original$',
            RenderThumbnail.as_view(), name='images_render_original'),
    url(r'^thumbnail/(?P<pk>\d+)/(?P<geometry>[0-9x]*)$',
            RenderThumbnail.as_view(), name='images_render_thumbnail'),
)
