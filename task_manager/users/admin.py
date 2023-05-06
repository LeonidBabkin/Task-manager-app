from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . models import NewUser


fields = list(UserAdmin.fieldsets)
fields[1] = ('Personal info', {'fields': ('first_name', 'last_name', 'age')})
UserAdmin.fieldsets = tuple(fields)
admin.site.register(NewUser, UserAdmin)
