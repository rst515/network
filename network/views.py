from datetime import datetime
import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import HttpResponse, HttpResponseRedirect, render
from django.urls import reverse
from django.db.models import Count
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt

from .forms import *
from .models import *
from django.contrib.auth.decorators import login_required

from django.db.models import Exists, OuterRef

def index(request):
    form = NewPost()
    posts = Post.objects.select_related('likes').annotate(num_Likes=Count('likedPost'),is_liked=Exists(Like.objects.filter(user=OuterRef('user_id')))).order_by("-timestamp").all()
    # like = Like.objects.get(user=request.user, post=p) 
    #likedOrNot = [True if Like.objects.filter(post=post.id, user=request.user) else False for post in posts]
    try:
        userLikes = [post.id if Like.objects.filter(post=post.id, user=request.user) else None for post in posts]
    except:
        userLikes = None
    print("userLikes :", posts[0].id, userLikes)

    paginator = Paginator(posts,10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)


    return render(request, "network/index.html", {
        "posts": page_obj,
        "form": form,
        "userLikes": userLikes,
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

@login_required
def addPost(request): 
    if request.method == "POST":
        form = NewPost(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)   # manually add 
            obj.user = request.user         # current user
            obj.save()                      # to form
            return index(request)
        else:
            return render(request, "network/index.html", {
                "form": form
            })
    else:
        return render(request, "network/index.html", {
            "form": NewPost()
        })    

@login_required
def addFollower(request):
    if (request.method == "POST"):
        u = User.objects.get(id=request.user.id)
        f = User.objects.get(id=request.POST['followUser'])
        follow = Follower.objects.create(user=u, follows=f)
        follow.save()
    return userPosts(request, f.id)

@login_required
def removeFollower(request):
    if (request.method == "POST"):
        u = User.objects.get(id=request.user.id)
        f = User.objects.get(id=request.POST['unfollowUser'])
        fx = Follower.objects.filter(user=u, follows=f)
        fx.delete()
    return userPosts(request, f.id)

@login_required
def deletePost(request):
    if (request.method == "POST"):
        fx = Post.objects.get(id=request.POST['post_id'], user=request.user)
        fx.delete()
    return index(request)

def userPosts(request, user_id):
    form = NewPost()
    user = User.objects.get(id=user_id)
    posts = Post.objects.filter(user=user_id).select_related('likes').annotate(num_Likes=Count('likedPost')).order_by("-timestamp").all()
    follows = Follower.objects.filter(user=user_id).annotate(num_Follows=Count('follows'))

    paginator = Paginator(posts,10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if not follows:
        follows = [0]
    followers = Follower.objects.filter(follows=user_id).annotate(num_Followers=Count('follows'))
    if not followers:
        followers = [0]
    if Follower.objects.filter(user=request.user, follows=user_id):
        is_followed = True
    else:
        is_followed = False
    #print("user.id :", user_id, "\nfollows: ", follows, "\nfollowers: ", followers, "\nis_followed :", is_followed, "\nlen Followers: ", len(followers), "\nlen Follows :", len(follows), "\nFollowers :", followers, "\nFollows :", follows)

    try:
        userLikes = [post.id if Like.objects.filter(post=post.id, user=request.user) else None for post in posts]
    except:
        userLikes = None

    return render(request, "network/user.html", {
    "user" : user,
    "posts": page_obj,
    "follows": len(follows),
    "followers": len(followers),
    "is_followed": is_followed,
    "form": form,
    "userLikes": userLikes,
})

@login_required
def following(request):
    followers = Follower.objects.filter(user=request.user.id)
    user_list = [follower.follows.id for follower in followers]
    posts = Post.objects.filter(user_id__in = user_list).select_related('likes').annotate(num_Likes=Count('likedPost')).order_by("-timestamp").all() 
    form = NewPost()
    try:
        userLikes = [post.id if Like.objects.filter(post=post.id, user=request.user) else None for post in posts]
    except:
        userLikes = None

    paginator = Paginator(posts,10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "network/index.html", {
        "posts": page_obj, #Post.objects.all(),
        "form": form,
        "userLikes": userLikes
            })

@login_required
@csrf_exempt
def editPost(request, post_id):
    # Query for requested post
    try:
        post = Post.objects.get(id=post_id) 
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)

    if request.method == "POST":
        post.subject = request.POST['edit_subject']
        post.body = request.POST['edit_post']
        post.save(update_fields=['body', 'subject'])
        print("Edited post: ", post)
        return HttpResponse(status=204)

    elif request.method == "GET":
        return JsonResponse(post.serialize())
    # Post must be via PUT
    else:
        return JsonResponse({
            "error": "PUT request required."
        }, status=400)

@csrf_exempt
@login_required
def post(request, post_id):
    # Query for requested post
    try:
        p = Post.objects.get(id=post_id)
        # Update whether post is liked or unliked
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)

    if request.method == "PUT":
        #see if like already exists, delete if it does
        try:
            like = Like.objects.get(user=request.user, post=p) 
        except Like.DoesNotExist:
            like = None

        if like:
            like.delete()
            return JsonResponse({"like": "Deleted."}) #HttpResponse(status=204), 
        else:
            u = User.objects.get(id=request.user.id)
            #p = Post.objects.get(id=data.get("post_id"))
            like = Like.objects.create(user=u, post=p)
            like.save()
            return JsonResponse({"like": "Created."}) #HttpResponse(status=204),

    elif request.method == "GET":
        return JsonResponse(p.serialize())

    # Post must be via PUT
    else:
        return JsonResponse({
            "error": "PUT request required."
        }, status=400)
    


@csrf_exempt
@login_required
def updateLikes(request, post_id):
        # Query for requested post
    try:
        p = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)

    if request.method == "GET":
        like = Like.objects.filter(post=p).count()
        return JsonResponse({'post_id':post_id,'likes':like})

    else:
        return JsonResponse({
            "error": "PUT request required."
        }, status=400)

