from django.contrib import admin
from .models import Photo

class PhotoAdmin(admin.ModelAdmin):
    readonly_fields = ['album_id', 'photo_id']

admin.site.register(Photo, PhotoAdmin)
