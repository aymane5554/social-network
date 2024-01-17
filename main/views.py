from django.shortcuts import render
from . import forms ,models
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
# Create signup page

def signup(request):
    if request.user.is_authenticated:
        return redirect('/logout')
    form = forms.User_form
    msg = ''
    if request.method == 'POST':
        form = forms.User_form(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/login')
        msg = 'wrong information'
        return render(request,"signup.html",{"form":form,'msg':msg})
    return render(request,"signup.html",{"form":form,'msg':msg})

# login page

def signin(request):
    if request.user.is_authenticated:
        return redirect('/logout')
    msg = ''
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request , username = username , password = password)
        if user :
            login(request,user)
            return redirect('/')
        msg = "Wrong Username or Password"
        return render(request,"login.html",{"msg":msg})
        
    return render(request,"login.html",{"msg":msg})

#log out 

@login_required(login_url="/login")
def logout_view(request):
    logout(request)
    return redirect("/")

# profile / friend list / edit delete posts / 

# user's feeds where he can post and see others posts
@login_required(login_url="/login")
@csrf_exempt
def home(request):
    image = ""
    msg = ""
    if request.method == "POST":
        if "post_submit" in request.POST:
            if request.POST["pc"] == "" and len(request.FILES) == 0:
                msg = 'post  cannot be empty'
                return render(request,"home.html",{"msg":msg})
            text = request.POST["pc"]
            if len(request.FILES) > 0 :
                image = request.FILES["pi"]
            user = request.user
            likes = 0 
            p = models.Post.objects.create(text = text , user=user , likes=likes , image=image)
            p.save() 
            return redirect('/')
        if 'comment_submit' in request.POST:
            text = request.POST["comment"]
            user = request.user
            post = request.POST["postId"]
            post = models.Post.objects.get(pk = post)
            p = models.Comments.objects.create(user=user,text=text,post=post)
            p.save()
            return redirect('/')

    return render(request,"home.html",{"msg":msg})

#profile
@login_required(login_url='/login')
def profile(request):
    user = request.user
    return render(request,"profile.html",{"user":user})

@login_required(login_url='/login')
def edit_profile(request):

    form = forms.Profile_form(instance = request.user)
    profile = models.User.objects.get(pk=request.user.id)
    if request.method == "POST":
        profile.username = request.POST["username"]
        profile.bio = request.POST["bio"]
        if len(request.FILES) > 0 :
            profile.image = request.FILES["image"]
        profile.save()
        return redirect("/profile")

    return render(request,"editprofile.html",{"form":form})

@login_required(login_url='/login')
def post_view(request,id):
    post = models.Post.objects.get(pk =id)
    comments = post.comments.all()
    return render(request,"post.html",{'post':post,'cmnts':comments}) 

@login_required(login_url="/login")
def others(request,name):
    var = 'add friend'
    user = models.User.objects.get(username =name)
    if user.id == request.user.id :
        return redirect("/profile") 
    if user in request.user.friends.all():
        var = "unfriend"
        return render(request,"others.html",{"user":user,"var":var})
    try:
        x = request.user.send.get(rec = user)
        var = "cancel request"
        return render(request,"others.html",{"user":user,"var":var})
    except models.Requests.DoesNotExist:
        pass
    try:
        x = request.user.rcvd.get(send = user)
        var = "accept request"
        return render(request,"others.html",{"user":user,"var":var})
    except models.Requests.DoesNotExist:
        pass
        
    return render(request,"others.html",{"user":user,"var":var})

@login_required(login_url="/login")
def add_friend(request,id):
    fr = models.User.objects.get(pk=id) 
    user = request.user
    if fr in user.friends.all():
        user.friends.remove(fr)
        return redirect(f"/account/{fr.username}")
    models.Requests.objects.create(send=request.user,rec=models.User.objects.get(pk=id))
    return redirect(f"/account/{fr.username}")

@login_required(login_url="/login")
def accept(request,id):
    fr = models.User.objects.get(pk=id) 
    if fr in request.user.friends.all():
        return redirect(f"/account/{fr.username}")
    request.user.friends.add(fr)    
    r = request.user.rcvd.get(send = fr)
    r.delete()
    return redirect(f"/account/{fr.username}")

@login_required(login_url="/login")
def cancel_request(request,id):
    user = models.User.objects.get(pk = id)
    r = request.user.send.get(rec = user)
    r.delete()
    return redirect(f"/account/{user.username}")

@login_required(login_url="/login")
def saveView(request):
    return render(request,"saves.html",)

@login_required(login_url="/login")
def edit_post(request,p):

    post  = models.Post.objects.get(pk = p)
    if request.method == "POST":
        if request.POST["text"] == "" and len(request.FILES) == 0:
            return render(request,"editpost.html",{"post" : post})
        text = request.POST["text"]
        if len(request.FILES) > 0 :
            image = request.FILES["img"]
            post.image = image
        post.text = text
        post.save() 
        return redirect("/profile")
    return render(request,"editpost.html",{"post" : post})


def search_result(request):
    txt = " "
    if request.method == "POST":
        txt = request.POST["search"]
        users = models.User.objects.filter(username__contains=txt)
        posts = models.Post.objects.filter(text__contains=txt)
        return render(request , "result.html" , {"txt" : txt , "users" : users , "posts" : posts})
    return render(request , "result.html" , {"txt" : txt})