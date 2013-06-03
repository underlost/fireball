from django.db import models
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.files.base import ContentFile
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

import datetime
import os
import urllib2
from urlparse import urlparse
from cStringIO import StringIO
from PIL import Image

from taggit.managers import TaggableManager

def upload_collection_header(instance, filename):
	return 'images/collections/%s/%s' % (instance.user.id, filename)

class Collection(models.Model):
	title = models.CharField(max_length=250)
	slug = models.SlugField(max_length=250)
	description = models.TextField(max_length=500, blank=True, null=True)
	user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='owned_collections')
	members = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, null=True, related_name='curator')
	pub_date = models.DateTimeField(auto_now_add=True)
	is_hidden = models.BooleanField(help_text=_("Should be checked if you dont want anyone to see."), default=False)
	tags = TaggableManager()
	
	def __unicode__(self):
		return "%s" % (self.name,)
		
	def get_absolute_url(self):
		return "/%s/%s/" % (self.owner, self.slug)    
	
	def save(self, *args, **kwargs):
		self.slug = slugify(self.title)
		super(Collection, self).save(*args, **kwargs)

	class Meta:
		ordering = ['-id']

def upload_original(instance, filename):
	return 'images/original/%s/%s' % (instance.user.id, filename)

def upload_thumb(instance, filename):
	return 'images/thumbnail/300/%s/%s' % (instance.user.id, filename)
			
class Blob(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL)
	url = models.TextField(blank=True, null=True)
	description = models.TextField(blank=True, null=True)
	image = models.ImageField(upload_to=upload_original)
	thumbnail = models.ImageField(upload_to=upload_thumb)
	pub_date = models.DateTimeField(auto_now_add=True)
	collection = models.ForeignKey(Collection, blank=True, null=True)
	tags = TaggableManager()

	def __unicode__(self):
		return self.url

	def create_thumbnail(self, content_type=None):
		# original code for this method came from
		# http://snipt.net/danfreak/generate-thumbnails-in-django-with-pil/
		# If there is no image associated with this.
		# do not create thumbnail
		if not self.image:
			return

		# Set our max thumbnail size in a tuple (max width, max height)
		THUMBNAIL_SIZE = (400, 1000)

		DJANGO_TYPE = content_type if content_type else self.image.file.content_type

		if DJANGO_TYPE == 'image/jpeg':
			PIL_TYPE = 'jpeg'
			FILE_EXTENSION = 'jpg'
		elif DJANGO_TYPE == 'image/png':
			PIL_TYPE = 'png'
			FILE_EXTENSION = 'png'

		# Open original photo which we want to thumbnail using PIL's Image
		image = Image.open(StringIO(self.image.read()))

		# We use our PIL Image object to create the thumbnail, which already
		# has a thumbnail() convenience method that contrains proportions.
		# Additionally, we use Image.ANTIALIAS to make the image look better.
		# Without antialiasing the image pattern artifacts may result.
		image.thumbnail(THUMBNAIL_SIZE, Image.ANTIALIAS)

		# Save the thumbnail
		temp_handle = StringIO()
		image.save(temp_handle, PIL_TYPE)
		temp_handle.seek(0)
		
		# Save image to a SimpleUploadedFile which can be saved into

		# ImageField
		suf = SimpleUploadedFile(os.path.split(self.image.name)[-1],
				temp_handle.read(), content_type=DJANGO_TYPE)
		# Save SimpleUploadedFile into image field
		self.thumbnail.save('%s_thumbnail.%s'%(os.path.splitext(suf.name)[0],FILE_EXTENSION), suf, save=False)

	def save(self):
		if not self.id:
			if self.url and not self.image:
				name = urlparse(self.url).path.split('/')[-1]
				extension = name.split('.')[-1]
				if extension == "jpg":
					content_type = "image/jpeg"
				elif extension == "png":
					content_type = "image/png"
				else:
					content_type = "text/plain"
					#TODO: Do something if this file isn't supported???
	
				#wrap your file content
				content = SimpleUploadedFile(name, urllib2.urlopen(self.url).read(), content_type=content_type)
				self.image.save(name, content, save=False)
	
				# create a thumbnail
				self.create_thumbnail(content_type)
			else:
				self.create_thumbnail()
		super(Blob, self).save() 


	class Meta:
		ordering = ['-id']

class Attachment(models.Model):
	blob = models.ForeignKey(Blob)
	user = models.ForeignKey(settings.AUTH_USER_MODEL)
	description = models.TextField(blank=True, null=True)
	pub_date = models.DateTimeField(auto_now_add=True)
	
	def get_absolute_url(self):
		return "/attachments/%s/" % (self.id)
		

class BlobView(models.Model):
    blob = models.ForeignKey(Blob, related_name='blobviews')
    ip = models.CharField(max_length=40)
    session = models.CharField(max_length=40)
    created = models.DateTimeField(default=datetime.datetime.now())
    