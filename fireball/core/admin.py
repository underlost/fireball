from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm
from .models import Profile

class ProfileChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = Profile

class ProfileAdmin(UserAdmin):
    form = ProfileChangeForm

    fieldsets = UserAdmin.fieldsets + (
            (None, {'fields': ('location', 'url', 'image', )}),
    )


admin.site.register(Profile, ProfileAdmin)