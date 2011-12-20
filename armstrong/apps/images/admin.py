from django.conf.urls.defaults import *
from django.contrib import admin
from django.views.generic import DetailView

from armstrong.core.arm_content.admin import fieldsets

from .models import Image, ImageSet, ImageSetElement
from .views import BrowseImages, BrowseImageSets, UploadImage

class ImageAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'image', 'summary'),
        }),

        fieldsets.TAXONOMY,
        fieldsets.PUBLICATION,
        fieldsets.AUTHORS,
    )

    def get_urls(self):
        urls = super(ImageAdmin, self).get_urls()
        browse_urls = patterns('',
            url(r'^browse/$',
                self.admin_site.admin_view(BrowseImages.as_view()),
                name='images_admin_browse'),
            url(r'^insert/(?P<pk>\d+)$',
                self.admin_site.admin_view(
                    DetailView.as_view(model=Image,
                        template_name='images/admin_insert.html')
                ), name='images_admin_insert'),
            url(r'^upload/$',
                self.admin_site.admin_view(UploadImage.as_view()),
                name='images_admin_upload'),
        )
        return browse_urls + urls

class ImageSetElementInline(admin.TabularInline):
    model = ImageSetElement
    raw_id_fields = ('image', )
        
class ImageSetAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'summary'),
        }),

        fieldsets.TAXONOMY,
        fieldsets.PUBLICATION,
        fieldsets.AUTHORS,
    )
    
    inlines = (ImageSetElementInline,)
    
    def get_urls(self):
        urls = super(ImageSetAdmin, self).get_urls()
        browse_urls = patterns('',
            url(r'^browse/$',
                self.admin_site.admin_view(BrowseImageSets.as_view()),
                name='imagesets_admin_browse'),
        )
        return browse_urls + urls
        
admin.site.register(Image, ImageAdmin)
admin.site.register(ImageSet, ImageSetAdmin)
