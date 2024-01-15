from rest_framework import serializers
from main.models import Post , Comments,User ,Reply,Notification

class Post_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"

class Comment_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = ['id','text','user','post']

class UserSerializer(serializers.ModelSerializer):
    class Meta :
        model = User
        fields = ["username","friends","bio","image","saves","posts"]

class ReplySerialier(serializers.ModelSerializer):
    class Meta :
        model = Reply
        fields = ["id","user","text",'comment']

class NotificationsSerialier(serializers.ModelSerializer):
    class Meta :
        model = Notification
        fields = ["text","link"]

