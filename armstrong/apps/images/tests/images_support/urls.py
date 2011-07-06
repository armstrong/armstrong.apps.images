from django.conf import settings
from django.conf.urls.defaults import *
from django.contrib import admin
from django.conf.urls.static import static


admin.autodiscover()

urlpatterns = patterns('',

    url(r'^images/', include('armstrong.apps.images.urls')),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login'),
    url(r'^admin/', include(admin.site.urls)),

) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
