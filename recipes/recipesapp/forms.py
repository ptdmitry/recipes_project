from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User

from .models import Recipe


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['name', 'description', 'cooking_steps', 'time_to_cook', 'picture', 'categories']


class ProfileForm(UserChangeForm):
    # Add additional fields specific to your profile model
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')
