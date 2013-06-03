from tastypie import fields
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie.authentication import BasicAuthentication
from tastypie.authorization import DjangoAuthorization

from fireball.blobs.models import Blob
from fireball.core.models import Profile

class UserResource(ModelResource):
	class Meta:
		queryset = Profile.objects.all()
		resource_name = 'user'
		excludes = ['email', 'password', 'is_superuser']
		# Add it here.
		authentication = BasicAuthentication()
		authorization = DjangoAuthorization()


class BlobResource(ModelResource):
	#user = fields.ForeignKey(UserResource, 'user')
	
	class Meta:
		queryset = Blob.objects.all()
		resource_name = 'blob'
		include_resource_uri = False
		filtering = {
			'pub_date': ['gt'],
		}

