from django.db import models
from django.contrib.auth.models import User
from django.conf.urls import url
from django.shortcuts import resolve_url


class UserProfileInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')

# Additional fields
    portfolio_site = models.URLField(blank=True)
    profile_pic = models.ImageField(upload_to='profile_pics', default="1.jpg")
    skills = models.CharField(max_length=300, null=True)

    def __str__(self):
        return self.user.username

