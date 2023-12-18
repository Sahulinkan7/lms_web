from django.contrib import admin
from .models import CustomUser
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

class Usermodel(UserAdmin):
    model=CustomUser

admin.site.register(User,UserAdmin)

admin.site.register(CustomUser)
