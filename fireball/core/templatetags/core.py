from __future__ import absolute_import
from urlparse import urlparse
import hashlib

from django import template
from django.shortcuts import redirect, render, get_object_or_404
from ..models import Profile

register = template.Library()

@register.filter
def base_site_url(value):                                        
	parsed = urlparse(value)
	return parsed.netloc

@register.filter
def email_hash(value):
	u = get_object_or_404(Profile, username=value)
	a = hashlib.md5(u.email).hexdigest()                                       
	return a
