from rest_framework import serializers
from main.models import Post , Comments,User

class Post_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"

class Comment_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = ['text','user','likes','reply','post']

class UserSerializer(serializers.ModelSerializer):
    class Meta :
        model = User
        fields = ["username","friends","bio","image","saves","posts"]