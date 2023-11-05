from django.contrib import admin
from .models import *

class UserAdmin(admin.ModelAdmin):
  list_display = ['name', 'password']

admin.site.register(User, UserAdmin)
