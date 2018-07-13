from django.contrib import admin
from .models import Group,GroupMember,Message, Request
# Register your models here.
admin.site.register(Group)
admin.site.register(GroupMember)
admin.site.register(Message)
admin.site.register(Request)

