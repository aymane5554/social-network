from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    image = models.ImageField(default="default.jpg")
    bio = models.TextField(blank=True,null=True)
    friends = models.ManyToManyField('self')
    saves = models.ManyToManyField('Post',related_name="saved_posts")

class Post(models.Model):
    text = models.TextField()
    image = models.ImageField(blank=True,null=True)
    is_share = models.BooleanField(default=False)
    shared = models.ForeignKey("self",blank=True , null = True , on_delete = models.CASCADE)
    user = models.ForeignKey(User,on_delete = models.CASCADE,related_name='posts')
    date = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default = 0)
    likers = models.ManyToManyField(User,related_name='likes')
    def __str__(self):
        return self.text

class Comments(models.Model):
    text = models.TextField(default="")
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    post = models.ForeignKey(Post,on_delete = models.CASCADE ,related_name="comments")

class Reply(models.Model):
    text = models.TextField(default="")
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    comment = models.ForeignKey(Comments,on_delete=models.CASCADE,related_name="reps")

class Notification(models.Model):
    text = models.TextField()
    user = models.ForeignKey(User,on_delete = models.CASCADE,related_name="notifications")
    link = models.CharField(max_length=60) 