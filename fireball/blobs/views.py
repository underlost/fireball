import datetime

from django.template.response import TemplateResponse
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.views.generic.list import ListView
from django.shortcuts import render_to_response, render, get_object_or_404, redirect
from django.template import RequestContext

from fireball.core.models import Profile
from taggit.models import Tag
from .forms import BlobForm
from .models import Blob, BlobView

class RecentView(ListView):
	paginate_by = 50
	template_name = 'blobs/blob_list.html'

	def get_queryset(self):
		return Blob.objects.order_by('-pub_date')

	def get_context_data(self, **kwargs):
		context = super(RecentView, self).get_context_data(**kwargs)
		context.update({'headers': False,})
		return context

class UserView(ListView):
	paginate_by = 50
	template_name = 'blobs/blob_list.html'

	def get_queryset(self):
		self.u = get_object_or_404(Profile, username=self.kwargs.pop('username'))
		self.latest = Blob.objects.filter(user__username=self.u).latest('pub_date')
		return Blob.objects.filter(user__username=self.u).order_by('-pub_date')

	def get_context_data(self, **kwargs):
		context = super(UserView, self).get_context_data(**kwargs)
		context.update({'headers': True, 'profile': True, 'user_obj': self.u, 'latest': self.latest,})
		return context

def SingleBlob(request, blob_id):
	blob = get_object_or_404(Blob, pk=blob_id)
	
	if not BlobView.objects.filter(blob=blob, session=request.session.session_key):
	        view = BlobView(blob=blob, ip=request.META['REMOTE_ADDR'], created=datetime.datetime.now(), session=request.session.session_key)
	        view.save()
	
	view_count = BlobView.objects.filter(blob=blob).count()
	tags = blob.tags.all()
	variables = RequestContext(request, {'object': blob, 'tags': tags, 'view_count': view_count,})
	return render_to_response('blobs/single_blob.html', variables)

def FullSizeBlob(request, blob_id):
	blob = get_object_or_404(Blob, pk=blob_id)
	variables = RequestContext(request, {'object': blob})
	return render_to_response('blobs/fullsize_blob.html', variables)
	
def infinite(request):
    return TemplateResponse(request, 'blobs/infinite.html', None)


def new_blob(request):
    if request.method == 'POST':
        form = BlobForm(request.POST, request.FILES)
        if form.is_valid():
            blob = form.save(commit=False)
            blob.user = request.user
            blob.save()
            messages.success(request, 'New blob successfully added.')
            return HttpResponseRedirect(reverse('blobs:home'))
        else:
            messages.error(request, 'Blob did not pass validation!')
    else:
        form = BlobForm()
    context = {
        'form': form,
    }
    return TemplateResponse(request, 'blobs/new_blob.html', context)


def delete_blob(request, blob_id):
    try:
        blob = Blob.objects.get(id=blob_id)
        if blob.user == request.user:
            blob.delete()
            messages.success(request, 'Blob successfully deleted.')
        else:
            messages.error(request, 'You are not the user and can not '
                                    'delete this blob.')
    except Blob.DoesNotExist:
        messages.error(request, 'Blob with the given id does not exist.')
        

    return HttpResponseRedirect(reverse('blobs:home'))
