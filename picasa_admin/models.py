from django.db import models
from django.conf import settings
from django.core.files import File
import os
import cStringIO, urllib2, Image
from django.core.files.temp import NamedTemporaryFile
import re

PICASA_ROOT = settings.PICASA_ROOT


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
            from .sender import save_to_picasa_server
            save_to_picasa_server.async(self.pk)

    def format_data(self):
        '''
        if has file clear url
        if no file download url to file clear url
        '''
        try:
            assert self.img, "no file"

        except Exception, e:
            print e
            
            #create a tempfile because the django filefield most be a named file can't use StringIO
            img_temp = NamedTemporaryFile(delete=True)
            img_temp.write(urllib2.urlopen(self.url).read())
            img_temp.flush()

            img_name = self.url.split('/')[-1].split('?')[0]
            self.img.save(img_name, File(img_temp))
        finally:
            self.url = ""


    def in_picasa(self):

        if self.album_id and self.photo_id:
            return True
        else re.search('https?://lh\d\.(ggpht|googleusercontent)\.com', self.url):
            try:
                data = cStringIO.StringIO(urllib2.urlopen(self.url).read())
                Image(data)
                self.album_id="out"
                self.photo_id="out"
            except Exception, e:
                return False
            else:
                return True
