from typing import Any, List, Optional
from django.contrib.admin.options import InlineModelAdmin
from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
# Register your models here.
from django.contrib.auth.models import User
from django.http.request import HttpRequest
from .models import Profile, Company

class ProfileInLine(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name = 'Perfil'
    verbose_name_plural = 'Perfiles'
    fk_name = 'user'

class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInLine,)

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        #return super().get_inline_instances(request, obj)
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('companyid', 'companyname')
    list_display_links = ('companyid', 'companyname')
    search_fields = ('companyid', 'companyname')
    list_per_page = 10

