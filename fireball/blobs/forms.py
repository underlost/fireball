from django import forms

from .models import Blob


class BlobForm(forms.ModelForm):
	url = forms.CharField(label='URL', required=False)
	image = forms.ImageField(label='or Upload', required=False)


	def __init__(self, *args, **kwargs):
		super(forms.ModelForm, self).__init__(*args, **kwargs)
		self.fields.keyOrder = (
			'url',
			'image',
			'description',
			'collection',
		)


	def check_if_image(self, data):
		# Test file type
		image_file_types = ['png', 'gif', 'jpeg', 'jpg']
		file_type = data.split('.')[-1]
		if file_type.lower() not in image_file_types:
			raise forms.ValidationError("Requested URL is not an image file. "
										"Only images are currently supported.")

	def clean(self):
		cleaned_data = super(BlobForm, self).clean()

		url = cleaned_data.get('url')
		image = cleaned_data.get('image')

		if url:
			self.check_if_image(url)
			try:
				Blob.objects.get(url=url)
				raise forms.ValidationError("URL has already been saved.")
			except Blob.DoesNotExist:
				try:
					Blob.objects.get(url=url)
					raise forms.ValidationError("URL has already been saved.")
				except Blob.DoesNotExist:
					pass
		elif image:
			pass
		else:
			raise forms.ValidationError("Need either a URL or Upload.")

		return cleaned_data

	class Meta:
		model = Blob
		exclude = ['user', 'thumbnail']
