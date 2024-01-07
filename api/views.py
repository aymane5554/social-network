from django.shortcuts import render
from .serializers import Post_Serializer , Comment_Serializer , UserSerializer
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from rest_framework.decorators import api_view
from main.models import Post , User ,Comments
from rest_framework.response import Response

# Create your views here.

@login_required(login_url="/login")
@api_view(["GET","PUT"])
def post_details(request,id):
    post = Post.objects.get(pk = id) 
    if request.method == "GET":
        serialize = Post_Serializer(post)
        JsonResponse(serialize.data , safe=False)
    if request.method == "PUT":
        if post in request.user.saves.all():
            request.user.saves.remove(post)
            serialize = Post_Serializer(post)
            JsonResponse(serialize.data , safe=False)
        
        request.user.saves.add(post)
        serialize = Post_Serializer(post)
        JsonResponse(serialize.data , safe=False)

@login_required(login_url="/login")
@api_view(["GET","POST"])
def CommentsApi(request,id):
    post = Post.objects.get(pk = id) 
    serialize = Comment_Serializer(post.comments.all().order_by('-id') , many=True)
    for i in range(len(serialize.data)): 
        user = User.objects.get(pk = serialize.data[i]["user"])
        serialize.data[i]["user"] = [serialize.data[i]["user"] , user.username,user.image.url]
    if request.method == 'POST':
        text = request.data['text']
        user  = request.user
        post = Post.objects.get(pk = request.data["post"])
        Comments.objects.create(text=text,user=user,post=post)
        return JsonResponse(serialize.data , safe=False)
    return Response(serialize.data)

@login_required(login_url="/login")
@api_view(["GET"])
def UserApi(request,id):
    u = User.objects.get(pk = id)
    serialize = UserSerializer(u)
    for i in range(len(serialize.data["friends"])):
        serialize.data["friends"][i] = User.objects.get(pk = serialize.data["friends"][i]).username
    serialize.data["posts"] = request.user.posts.all()
    return JsonResponse(serialize.data,safe=False)

def time(item):
    return item.date

@login_required(login_url="/login")
@api_view(["GET"])
def feed(request):
    posts = []
    posts.extend(request.user.posts.all())
    friends = request.user.friends.all()
    for friend in friends:
        posts.extend(friend.posts.all())
    posts.sort(reverse=True,key=time)
    serialize = Post_Serializer(posts,many=True)
    for i in range(len(serialize.data)):
        user = User.objects.get(pk = serialize.data[i]["user"])
        serialize.data[i]["user"] = [serialize.data[i]["user"] , user.username,user.image.url]
    return JsonResponse(serialize.data,safe=False)

@login_required(login_url="/login")
@api_view(["GET"])
def prpo(request,id):
    posts = Post.objects.filter(user = User.objects.get(username = id)).order_by("-id")
    serialize = Post_Serializer(posts,many = True)
    for i in range(len(serialize.data)):
        user = User.objects.get(pk = serialize.data[i]["user"])
        serialize.data[i]["user"] = [serialize.data[i]["user"] , user.username,user.image.url]
    return JsonResponse(serialize.data , safe=False)