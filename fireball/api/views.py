from django.utils import simplejson
from django.http import HttpResponse , HttpResponseRedirect
from fireball.blobs.models import Blob
from django.core.files import File
from django.core.files.images import ImageFile
from django.template.response import TemplateResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import redirect_to_login 
from django.contrib.auth.models import User
import urllib2
import hashlib

def blobs_user_recent(request, user_id=1, page=1):
    start_blob = abs(int(page) - 1) * 25
    end_blob = int(page) * 25

    blobs = Blob.objects.order_by('-id').filter(author=user_id)
    recent_blobs = []
    for blob in blobs:
        recent_blobs.append({
            'id': blob.id,
            'thumbnail': blob.image.url.rstrip('.jpg')+".200x1000.jpg",
            'original': blob.image.url,
            'description': blob.description,
            'username' : blob.user.username,
        })

    return HttpResponse(simplejson.dumps(recent_blobs), mimetype="application/json")

def blobs_recent(request, page=1):
    start_blob = abs(int(page) - 1) * 25
    end_blob = int(page) * 25

    blobs = Blob.objects.order_by('-id')[start_blob:end_blob]
        
    recent_blobs = []
    for blob in blobs:
        recent_blobs.append({
            'id': blob.id,
            'thumbnail': blob.thumbnail.url,
            'image': blob.image.url,
            'description': blob.description,
            'url': blob.url,
            'username' : blob.user.username,
            'user_id' : blob.user.id,
            'email_hash': hashlib.md5(blob.user.email).hexdigest(),
        })

    return HttpResponse(simplejson.dumps(recent_blobs), mimetype="application/json")