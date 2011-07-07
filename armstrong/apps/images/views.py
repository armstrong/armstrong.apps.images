import operator
from django.contrib.admin.views.decorators import staff_member_required
from django.template import RequestContext
from django.db import models
from django.views.generic import ListView, CreateView
from django.core.urlresolvers import reverse
from .models import Image


class BrowseImages(ListView):
    
    model = Image
    template_name = 'images/admin_browse.html'
    paginate_by = 32

    def get_queryset(self):

        fields = ['title', 'caption']
        query = self.request.GET.get('q')
        images = super(BrowseImages, self).get_queryset().order_by('-created')

        if not query:
            return images

        outer_q = []
        for token in query.split():
            inner_q = []
            for field in fields:
                inner_q.append(models.Q(**{field + '__icontains': token}))
            outer_q.append(reduce(operator.or_, inner_q))

        return images.filter(reduce(operator.and_, outer_q))


class UploadImage(CreateView):

    model = Image
    template_name = 'images/admin_upload.html'

    def get_success_url(self):

        if self.success_url:
            return super(UploadImage, self).get_success_url(self)
        else:
            return reverse('images_admin_insert',
                    kwargs={'pk': self.object.id})
