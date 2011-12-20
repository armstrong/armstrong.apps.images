import random
import os.path
import datetime

from django.conf import settings
from django.core.files import File

from ..models import Image, ImageSet, ImageSetElement

LOCAL_IMAGE_PATH = os.path.join(os.path.dirname(__file__),
                                'support', 'smiley.jpg')
SERVER_IMAGE_PATH = os.path.join(settings.MEDIA_ROOT,
                                 settings.ARMSTRONG_IMAGES_UPLOAD_PATH,
                                'smiley.jpg')


def generate_random_image():
    title = 'Random title %s' % random.randint(100, 1000)
    summary = 'Random summary %s' % random.randint(100, 1000)
    pub_date = datetime.datetime.now()
    f = open(LOCAL_IMAGE_PATH)
    with open(LOCAL_IMAGE_PATH) as f:
        im = Image.objects.create(title=title, summary=summary,
                                  pub_date=pub_date, image=File(f))
    return im

def generate_random_imageset():
    title = 'Random title %s' % random.randint(100, 1000)
    summary = 'Random summary %s' % random.randint(100, 1000)
    pub_date = datetime.datetime.now()
    
    iset = ImageSet.objects.create(title=title, summary=summary,
                                   pub_date=pub_date)
    
    cnt = 1
    for image in Image.objects.all().order_by('?')[:random.randint(2, 5)]:
      caption = 'Random caption %s' % random.randint(100, 1000)
      iele = ImageSetElement.objects.create(image=image, imageset=iset,
                                            caption=caption, order=cnt)
      
      cnt += 1
      
    return iset