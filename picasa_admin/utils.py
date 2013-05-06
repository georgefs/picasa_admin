#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2013 george 
#
# Distributed under terms of the MIT license.
import re
import Image
from .picasa_storage import PicasaStorage
from django.conf import settings

def in_picasa(url):
    return re.search('https?://lh\d\.(ggpht|googleusercontent)\.com/.*\d+x\d+(.jpg)?$', url)

picasa_storage = None
def get_picasa_storage():
    global picasa_storage
    if not picasa_storage:
        reset_pisca_storage()
    return picasa_storage
def reset_pisca_storage():
    global picasa_storage
    print 'logining'
    picasa_storage = PicasaStorage(settings.PICASA_USER, settings.PICASA_PASSWORD)
    print 'logined'


def send_photo(photo, count=0):
    try:
        print photo
        ps = get_picasa_storage()
        print 'send'
        result= ps.insert_photo(photo)
        count=0
        return result
    except IOError,e:
        print "not image"
        raise e
    except Exception, e:
        print e
        if count==2:
            count=0
            raise Exception('can"t insert')
        reset_pisca_storage()
        send_photo(photo, count+1)
        
