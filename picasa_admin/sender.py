__all__ = ['save_to_picasa_server']
from django.conf import settings
from django_ztask.decorators import task
from .picasa_storage import PicasaStorage
from .models import Photo

picasa_storage = None
def get_picasa_storage():
    global picasa_storage
    picasa_storage = picasa_storage if picasa_storage else PicasaStorage(settings.PICASA_USER, settings.PICASA_PASSWORD)
    return picasa_storage


@task()
def save_to_picasa_server(pk):
    '''
        sync Photo image to picasa server
        pk = Photo Model key
    '''

    ps = get_picasa_storage()

    photo = Photo.objects.get(pk=pk)
    photo_path = photo.img.name
    picasa_photo = ps.insert_photo(photo_path)
    photo.album_id = picasa_photo.albumid.text
    photo.photo_id = picasa_photo.gphoto_id.text
    photo.url = picasa_photo.content.src

    photo.save()

