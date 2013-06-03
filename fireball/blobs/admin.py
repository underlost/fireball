from django.contrib import admin
from fireball.blobs.models import Blob

class BlobAdmin(admin.ModelAdmin):
   list_filter = ('user',)
   search_fields = ['description','url',]
   list_display = ('user', 'url',) 
admin.site.register(Blob,BlobAdmin)

