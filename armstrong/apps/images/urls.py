from django.conf.urls.defaults import *
from django.views.generic import DetailView, CreateView
from .models import Image
from .views import BrowseImages, UploadImage


urlpatterns = patterns('',

    #TODO: enforce is_staff or has_permission? 
    url(r'^admin/browse/$', BrowseImages.as_view(), name='images_admin_browse'),

    url(r'^admin/insert/(?P<pk>\d+)$', DetailView.as_view(
            model=Image,
            template_name='images/admin_insert.html'
    ),  name='images_admin_insert'),

    url(r'^admin/upload/$', UploadImage.as_view(), name='images_admin_upload'),
)
