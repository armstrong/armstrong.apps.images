from django.conf.urls.defaults import *
from django.views.generic import DetailView, CreateView
from django.contrib.auth.decorators import permission_required
from .models import Image
from .views import BrowseImages, UploadImage, RenderThumbnail


urlpatterns = patterns('',

    url(r'^admin/browse/$',
            permission_required('images.add_image')(BrowseImages.as_view()),
            name='images_admin_browse'),

    url(r'^admin/insert/(?P<pk>\d+)$', permission_required('images.add_image')(
            DetailView.as_view(model=Image,
                template_name='images/admin_insert.html')),
            name='images_admin_insert'),

    url(r'^admin/upload/$', permission_required('images.add_image')(
            UploadImage.as_view()), name='images_admin_upload'),


    url(r'^thumbnail/(?P<pk>\d+)/(?P<geometry>[0-9x]+)',
            RenderThumbnail.as_view(), name='images_render_thumbnail'),

)
