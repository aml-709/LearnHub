from django.contrib import admin
from django.urls import path, include
from . import views
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model
from .models import User, Course, Section, Lesson


User = get_user_model()

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    pass

admin.site.register(Course)

