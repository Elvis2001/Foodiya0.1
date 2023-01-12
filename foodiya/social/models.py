from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    user_first_name = models.TextField(max_length=50, null=True, blank=True)
    user_last_name = models.TextField(max_length=50, null=True, blank=True)
    profile_picture = models.ImageField(upload_to='media/profile_pic', default='media/default.png')
    profile_bio = models.TextField(max_length=50, null=True, blank=True)
    user_email = models.EmailField(max_length=25, null=True, blank=True)
    user_birth_date = models.DateField(null=True, blank=True)
    created_updated = models.DateField(auto_now_add=True)
    followers = models.ManyToManyField(User, blank=True, related_name='followers')
    following = models.ManyToManyField(User, blank=True, related_name='following')


#    def __str__(self):
 #       return self.user

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()



class PostFileContent(models.Model):
    user = models.ForeignKey(User, related_name='content_owner', on_delete=models.CASCADE)
    file = models.FileField(upload_to='media/profile_pics')

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    pic_or_vid = models.ManyToManyField(PostFileContent, related_name='contents')
    post_caption = models.TextField(max_length=80, verbose_name='Caption')
    date_post_posted = models.DateTimeField(auto_now_add=True)
    likes=models.ManyToManyField(User, blank=True, related_name='likes')
    dislikes = models.ManyToManyField(User, blank=True, related_name='dislikes')


    #def __str__(self):
     #   return f'{self.author} posts'

    #def get_absolute_url(self):
     #   return reverse('postdetails', kwargs={'pk':self.pk})

 
class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE,)
    comment = models.TextField(max_length= 100)
    date_of_comment = models.DateTimeField(auto_now_add=True)

    #likes
    #dislikes



class Notification(models.Model):
    Notification_type = ((1, 'comment'), (2, 'follow'), (3, 'like'))


    to_user = models.ForeignKey(User, related_name='notification_to', on_delete=models.CASCADE, null=True)
    from_user = models.ForeignKey(User, related_name='notification_from', on_delete=models.CASCADE, null=True)
    comment = models.ForeignKey('Comment', related_name='+', on_delete=models.CASCADE)
    post = models.ForeignKey('Post', related_name='+', on_delete=models.CASCADE)
    date_time = models.DateTimeField(auto_now_add=True)
    text = models.TextField(max_length=50)
    notification_type = models.IntegerField(choices=Notification_type)
    is_seen = models.BooleanField(default=False)
