from django.db import models
from posts.models import Posts
from accounts.models import UserProfileInfo
from django.utils.text import slugify
from django.db.models.signals import post_save

# Create your models here.


class Group(models.Model):
    project = models.OneToOneField(Posts, on_delete=models.CASCADE, related_name='group')
    slug = models.SlugField(allow_unicode=True, unique=True)
    name = models.CharField(max_length=200, default='New Group')
    members = models.ManyToManyField(UserProfileInfo, through='GroupMember', related_name='groups')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)


def post_save_posts_model_receiver(sender, instance, created, *args, **kwargs):
    if created:
        try:
            Group.objects.create(project=instance, name=instance.project_title+' group')
        except:
            pass


post_save.connect(post_save_posts_model_receiver, sender=Posts)


class GroupMember(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='group_members')
    profile = models.ForeignKey(UserProfileInfo, on_delete=models.CASCADE, related_name='group_member')
    admin = models.BooleanField(default=False)

    def __str__(self):
        return self.profile.user.username


def post_save_group_model_receiver(sender, instance, created, *args, **kwargs):
    if created:
        try:
            GroupMember.objects.create(group=instance, profile=instance.project.profile, admin=True)
        except:
            pass


post_save.connect(post_save_group_model_receiver, sender=Group)


class Message(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='messages')
    user = models.ForeignKey(UserProfileInfo, on_delete=models.CASCADE, related_name='messages')
    text = models.TextField()
    sent_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    class Meta:
        unique_together = ['user', 'text']


class Request(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='requests')
    sent_by = models.ForeignKey(UserProfileInfo, on_delete=models.CASCADE, related_name='requests')
    sent_at = models.DateTimeField(auto_now=True)
    accepted = models.BooleanField(default=False)

    def __str__(self):
        return self.sent_by.user.username

    def accept(self):
        self.accepted = True
        self.save()
        GroupMember.objects.create(group=self.group, profile=self.sent_by, admin=False)
