from django.db import models
from django.contrib.auth.models import User
from django.db.models import Manager


class Recipe(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    cooking_steps = models.TextField()
    time_to_cook = models.PositiveIntegerField()  # Time in minutes
    picture = models.ImageField(upload_to='recipe_images/', null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    categories = models.ManyToManyField('Category')
    objects = Manager()

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100)
    objects = Manager()

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    objects = Manager()

    def __str__(self):
        return self.user.username
