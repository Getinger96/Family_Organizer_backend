from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Child

admin.site.register(User, UserAdmin)
# Register your models here.
admin.site.register(Child)