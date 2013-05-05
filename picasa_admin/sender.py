__all__ = ['save_to_picasa_server']
from django.conf import settings
from django_ztask.decorators import task
from .models import Photo
from .utils import send_photo



@task()
def save_to_picasa_server(pk):
    '''
        sync Photo image to picasa server
        pk = Photo Model key
    '''


    photo = Photo.objects.get(pk=pk)
    photo_path = photo.img.name
    picasa_photo = send_photo(photo_path)
    photo.album_id = picasa_photo.albumid.text
    photo.photo_id = picasa_photo.gphoto_id.text
    photo.url = picasa_photo.content.src

    photo.save()

