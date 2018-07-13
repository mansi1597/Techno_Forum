from django.db import models
from accounts.models import UserProfileInfo
from django.utils import timezone
from django.urls import reverse
# Create your models here.


class Posts(models.Model):
    profile = models.ForeignKey(UserProfileInfo, on_delete=models.CASCADE, related_name='posts')
    project_title = models.CharField(max_length=200)
    project_description = models.TextField()
    skills_required = models.TextField()
    members_required = models.IntegerField()
    posted_on = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.project_title

    def get_absolute_url(self):
        return reverse('posts:list_and_create', kwargs={'pk': self.profile.pk})


class Comments(models.Model):
    post = models.ForeignKey(Posts, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(UserProfileInfo, on_delete=models.CASCADE, related_name='user_comments')
    comment_text = models.TextField()
    comment_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.comment_text

    def get_absolute_url(self):
        return reverse('posts:post_detail', kwargs={'pk': self.post.pk})

