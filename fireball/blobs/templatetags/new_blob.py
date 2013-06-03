from django.template.loader import render_to_string
from django.template import Library
from django.template import RequestContext

from fireball.blobs.forms import BlobForm


register = Library()


@register.simple_tag
def new_blob(request):
    return render_to_string('blobs/templatetags/new_blob.html',
        {'form': BlobForm()},
        context_instance=RequestContext(request))
