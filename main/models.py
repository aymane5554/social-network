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
    user = models.ForeignKey(User,on_delete = models.CASCADE,related_name='posts')
    date = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default = 0)
    def __str__(self):
        return self.text

class Comments(models.Model):
    text = models.TextField(default="")
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    reply = models.OneToOneField('self',on_delete=models.CASCADE,blank=True,null=True)
    post = models.ForeignKey(Post,on_delete = models.CASCADE ,related_name="comments")
    likes = models.IntegerField(default = 0)
