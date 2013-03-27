from django.db import models
from django.conf import settings
from django.core.files import File
import os
import cStringIO, urllib2, Image
from django.core.files.temp import NamedTemporaryFile
from django_ztask.decorators import task
import time
from .picasa_storage import PicasaStorage

PICASA_ROOT = settings.PICASA_ROOT


ps = PicasaStorage(settings.PICASA_USER, settings.PICASA_PASSWORD)
@task()
def send_picasa(pk):
    '''
        send photo to picasa server
    '''
    photo = Photo.objects.get(pk=pk)
    photo_path = photo.img.name
    picasa_photo = ps.insert_photo(photo_path)
    photo.album_id = picasa_photo.albumid.text
    photo.photo_id = picasa_photo.gphoto_id.text
    photo.url = picasa_photo.content.src

    photo.save()


# Create your models here.


class Photo( models.Model ): 
    url = models.URLField(null=True, blank=True)
    img = models.ImageField(upload_to=PICASA_ROOT, null=True, blank=True)
    album_id = models.CharField(max_length=200, null=True, blank=True)
    photo_id = models.CharField(max_length=200, null=True, blank=True)

    def __unicode__(self):
        return self.img.name


    def save(self):

        if not self.in_picasa():
            self.format_data()

        super(Photo, self).save()

        if not self.in_picasa():
            send_picasa.async(self.pk)

    def format_data(self):
        '''
        if has file clear url
        if no file download url to file clear url
        '''
        try:
            assert self.img, "no file"

        except Exception, e:
            print e
            
            img_temp = NamedTemporaryFile(delete=True)
            img_temp.write(urllib2.urlopen(self.url).read())
            img_temp.flush()

            img_name = self.url.split('/')[-1].split('?')[0]
            self.img.save(img_name, File(img_temp))
        finally:
            self.url = ""


    def in_picasa(self):
        return self.album_id and self.photo_id


