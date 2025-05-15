from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from .models import Course, Section, Lesson

User = get_user_model()

class RegisterForm(UserCreationForm):
    role = forms.ChoiceField(choices=User.ROLE_CHOICES, required=True, label="Role")

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'role']

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'description']


class SectionForm(forms.ModelForm):
    class Meta:
        model = Section
        fields = ['title']

class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['title', 'content', 'image', 'order']



