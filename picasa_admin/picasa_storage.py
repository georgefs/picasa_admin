import gdata.photos.service
import Image
import collections, functools

__all__ = ["PicasaStorage", ]

class memoized(object):
    '''Decorator. Caches a function's return value each time it is called.
    If called later with the same arguments, the cached value is returned
    (not reevaluated).
    '''
    def __init__(self, func):
        self.func = func
        self.cache = {}
    def __call__(self, *args):
        if not isinstance(args, collections.Hashable):
            # uncacheable. a list, for instance.
            # better to not cache than blow up.
            return self.func(*args)
        self.cache[args] = self.cache[args] if self.cache.get(args, False) else self.func(*args)

        return self.cache[args]

    def __repr__(self):
        '''Return the function's docstring.'''
        return self.func.__doc__
    def __get__(self, obj, objtype):
        '''Support instance methods.'''
        return functools.partial(self.__call__, obj)


class PicasaStorage:
    '''
    simple way to use google picasa save your img

    photo_storage = PicasaStorage("email", "password")
    photo = photo_storage.insert_photo("path.jpg")
    
    print photo.content.src

    '''
    

    waitting_album_list = None
    current_album = None

    def __init__(self, email, password, username="default"):

        self.username = username    

        self._ = gdata.photos.service.PhotosService()
        self._.ClientLogin(email, password)

        self.waitting_album_list = self.scan_albums()
        self.current_album = self.waitting_album_list.next()


    def create_album(self, title="data", summary="photo storage"):
        album = self._.InsertAlbum(title=title, summary=summary)
        album.length = 0
        return album


    def __get_albums_size(self, album):
        photos = self.get_album_photos(album)
        album_photos_length = len(photos)
        return album_photos_length
    
    @memoized
    def get_album_photos(self, album):
        photos = self._.GetFeed("/data/feed/api/user/{}/albumid/{}?kind=photo".format(self.username ,album.gphoto_id.text)).entry
        return photos

    @memoized
    def get_album_photo(self, album_id, photo_id):
        album = self.get_album(album_id)
        photos = self.get_album_photos(album)

        for photo in photos:
            if(photo_id == photo.gphoto_id.text):
                return photo

    @memoized
    def get_albums(self):
        albums = self._.GetUserFeed(user = self.username)
        return albums.entry
    
    @memoized
    def get_album(self, album_id):
        for album in self.get_albums():
            if(album_id ==album.gphoto_id.text):
                return album

    def scan_albums(self):
        '''
            search album who has space to save photo

            if all album is full, then create new album to storage photos
        '''

        albums = self.get_albums()

        for album in albums:
            album.length = self.__get_albums_size(album)
            if album.length >= 1000:
                continue
            else:
                yield album

        yield self.create_album()

    def remove_photo(self, photo):
        self._.Delete(photo)

    def insert_photo(self, filename, title = None , summary = "photo storage", content_type='image/jpeg'):
        try:
            
            if(title == None):
                title="{}x{}".format(*Image.open(filename).size)

            self.current_album = self.current_album if self.current_album.length < 1000 else self.waitting_album_list.next()

            album_url = "'/data/feed/api/user/{}/albumid/{}'".format(self.username, self.current_album.gphoto_id.text)
            photo = self._.InsertPhotoSimple(self.current_album, title, summary, filename,  content_type)

        except Exception, e:
            self.insert_photo(filename, title, summary, content_type)

        else:
            self.current_album.length += 1
            return photo

        



if __name__ == "__main__":
    ps = PicasaStorage()
    #photo = ps.insert_photo('/tmp/1.jpg')
