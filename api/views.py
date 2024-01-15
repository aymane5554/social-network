from django.shortcuts import render
from .serializers import Post_Serializer , Comment_Serializer , UserSerializer ,ReplySerialier ,NotificationsSerialier 
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from rest_framework.decorators import api_view
from main.models import Post , User ,Comments ,Reply,Notification
# Create your views here.

@login_required(login_url="/login")
@api_view(["GET","PUT","DELETE"])
def post_details(request,id):
    post = Post.objects.get(pk = id) 
    if request.method == "GET":
        serialize = Post_Serializer(post)
        return JsonResponse(serialize.data , safe=False)
    elif request.method == "PUT":
        if request.data == "save":
            if post in request.user.saves.all():
                request.user.saves.remove(post)
                serialize = Post_Serializer(post)
                return JsonResponse(serialize.data , safe=False)
            request.user.saves.add(post)
            serialize = Post_Serializer(post)
            return JsonResponse(serialize.data , safe=False)
            
        elif request.data == "like":
            if request.user in post.likers.all():
                post.likes -= 1
                post.likers.remove(request.user)
                post.save()
                serialize = Post_Serializer(post)
                return JsonResponse(serialize.data , safe=False)
            
            post.likes += 1 
            post.likers.add(request.user)
            post.save()
            serialize = Post_Serializer(post)
            return JsonResponse(serialize.data , safe=False)
        serialize = Post_Serializer(post)
        return JsonResponse(serialize.data , safe=False)
    if request.method == "DELETE":
        post.delete()
        return JsonResponse({"post" : "deleted"})

@login_required(login_url="/login")
@api_view(["GET","POST"])
def CommentsApi(request,id):
    post = Post.objects.get(pk = id) 
    serialize = Comment_Serializer(post.comments.all().order_by('-id') , many=True)
    for i in range(len(serialize.data)): 
        user = User.objects.get(pk = serialize.data[i]["user"])
        serialize.data[i]["user"] = [serialize.data[i]["user"] , user.username,user.image.url]
        cmnt =  Comments.objects.get(pk = serialize.data[i]["id"])
        serialize.data[i]["reply"] = ReplySerialier(cmnt.reps.all(),many=True).data
    if request.method == 'POST':
        text = request.data['text']
        user  = request.user
        post = Post.objects.get(pk = request.data["post"])
        if request.data["reply"] != None :
            ree = Reply.objects.create(text=text,user=user,comment = Comments.objects.get(pk=request.data["reply"]))
            ree.save()
            serialize = ReplySerialier(ree)
            return JsonResponse(serialize.data , safe=False)
        cc = Comments.objects.create(text=text,user=user,post=post)
        serialize = Comment_Serializer(cc)
        return JsonResponse(serialize.data , safe=False)
    return JsonResponse(serialize.data ,safe=False)

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
        if serialize.data[i]["is_share"] == True:
            p = Post.objects.get(pk = serialize.data[i]["shared"])
            if p.image == None :
                serialize.data[i]["shared"] = [serialize.data[i]["shared"],p.user.username,p.user.image.url,p.text,None]
            else : 
                s =  Post_Serializer(p)
                img = s.data["image"]
                
                serialize.data[i]["shared"] = [serialize.data[i]["shared"],p.user.username,p.user.image.url,p.text,img]     
    return JsonResponse(serialize.data,safe=False)

@login_required(login_url="/login")
@api_view(["GET"])
def prpo(request,id):
    posts = Post.objects.filter(user = User.objects.get(username = id)).order_by("-id")
    serialize = Post_Serializer(posts,many = True)
    for i in range(len(serialize.data)):
        user = User.objects.get(pk = serialize.data[i]["user"])
        serialize.data[i]["user"] = [serialize.data[i]["user"] , user.username,user.image.url]
        if serialize.data[i]["is_share"] == True:
            p = Post.objects.get(pk = serialize.data[i]["shared"])
            if p.image == None :
                serialize.data[i]["shared"] = [serialize.data[i]["shared"],p.user.username,p.user.image.url,p.text,None]
            else : 
                s =  Post_Serializer(p)
                img = s.data["image"]
                
                serialize.data[i]["shared"] = [serialize.data[i]["shared"],p.user.username,p.user.image.url,p.text,img]  
    return JsonResponse(serialize.data , safe=False)

@login_required(login_url="/login")
@api_view(["GET"])
def saved(request):
    posts = request.user.saves.all()
    serialize = Post_Serializer(posts , many=True)
    for i in range(len(serialize.data)):
        user = User.objects.get(pk = serialize.data[i]["user"])
        serialize.data[i]["user"] = [serialize.data[i]["user"] , user.username,user.image.url]
        if serialize.data[i]["is_share"] == True:
            p = Post.objects.get(pk = serialize.data[i]["shared"])
            if p.image == None :
                serialize.data[i]["shared"] = [serialize.data[i]["shared"],p.user.username,p.user.image.url,p.text,None]
            else : 
                s =  Post_Serializer(p)
                img = s.data["image"]
                
                serialize.data[i]["shared"] = [serialize.data[i]["shared"],p.user.username,p.user.image.url,p.text,img]  
    return JsonResponse(serialize.data , safe=False)

@login_required(login_url="/login")
@api_view(["POST"])
def share_view(request):
    if request.method == "POST":
        text = request.data["text"]
        user = request.user
        shared = Post.objects.get(pk=request.data["id"])
        p = Post.objects.create(text=text,is_share= True,shared = shared,user=user)
        p.save()
        serialize = Post_Serializer(p)
        return JsonResponse(serialize.data,safe=False)
    
@login_required(login_url="/login")
@api_view(["GET","POST"])
def inboxApi(request):
    if request.method == "GET":
        n = request.user.notifications.all().order_by("-id")
        serializer = NotificationsSerialier(n,many=True)
        return JsonResponse(serializer.data,safe=False)
    if request.method == "POST":
        text = request.data["note"]
        id = request.data["id"]
        if text == "share":
            text = f"{request.user.username} shared your post"
            user = Post.objects.get(pk = id).user
            nn =Notification.objects.create(text=text,user=user,link=f"/p/{Post.objects.get(pk = id).id}/")
            nn.save()
            n = request.user.notifications.all()
            serializer = NotificationsSerialier(n,many=True)
        elif text == "like":
            text = f"{request.user.username} liked your post"
            user = Post.objects.get(pk = id).user
            if request.user in Post.objects.get(pk = id).likers.all() : 
                nn =Notification.objects.create(text=text,user=user ,link=f"/p/{Post.objects.get(pk = id).id}/")
                nn.save()
            n = request.user.notifications.all()
            serializer = NotificationsSerialier(n,many=True)
        elif text == "comment":
            text = f"{request.user.username} commented to your post"
            user = Post.objects.get(pk = id).user
            nn =Notification.objects.create(text=text,user=user, link=f"/p/{Post.objects.get(pk = id).id}/")
            nn.save()
            n = request.user.notifications.all()
            serializer = NotificationsSerialier(n,many=True)
        elif text == "reply":
            text = f"{request.user.username} replied to your comment"
            user = Comments.objects.get(pk = id).user
            p = Comments.objects.get(pk = id).post.id
            nn =Notification.objects.create(text=text,user=user,link=f"/p/{id}/" )
            nn.save()
            n = request.user.notifications.all()
            serializer = NotificationsSerialier(n,many=True)
        return JsonResponse(serializer.data,safe=False)
    