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

        query = self.request.GET.get('q')
        qs = super(BrowseImages, self).get_queryset()

        if not query:
            return qs

        queries = []

        for token in query.split():
            queries.append(models.Q(title__icontains=token))

        return qs.filter(reduce(operator.and_, queries)).order_by('-created')

class UploadImage(CreateView):

    model = Image
    template_name = 'images/admin_upload.html'

    def get_success_url(self):

        if self.success_url:
            return super(UploadImage, self).get_success_url(self)
        else:
            return reverse('images_admin_insert', kwargs={'pk': self.object.id})
