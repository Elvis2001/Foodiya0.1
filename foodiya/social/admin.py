from django.contrib import admin
from .models import UserProfile, Notification, Comment, Post, PostFileContent

admin.site.register(UserProfile)
admin.site.register(Notification)
admin.site.register(Comment)
admin.site.register(Post)
admin.site.register(PostFileContent)
