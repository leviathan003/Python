from django.shortcuts import render,redirect
from django.contrib.auth.models import User, auth 
from django.http import HttpResponse
from django.contrib import messages
from .models import Profile,Post,like_post,followersCount,Comment
from django.contrib.auth.decorators import login_required
from itertools import chain
import random

# Create your views here.
@login_required(login_url='signin')
def index(request):
    user_object=User.objects.get(username=request.user.username)
    user_profile=Profile.objects.get(user=user_object)

    user_following_list=[]
    feed=[]
    user_following=followersCount.objects.filter(follower=request.user.username)

    for users in user_following:
        user_following_list.append(users.user)

    for usernames in user_following:
        feedlist=Post.objects.filter(user=usernames)
        feed.append(feedlist)

    feedlists=list(chain(*feed))

    #user-suggestions
    all_users=User.objects.all()
    user_following_all=[]

    for user in user_following:
        user_list=User.objects.get(username=user.user)
        user_following_all.append(user_list)

    new_suggestion_list=[x for x in list(all_users) if ( x not in list(user_following_all))]
    current_user=User.objects.filter(username=request.user.username)
    final_suggestions_list = [x for x in list(new_suggestion_list) if (x not in list(current_user))]
    random.shuffle(final_suggestions_list)

    username_profile=[]
    username_profile_list=[]

    for users in final_suggestions_list:
        username_profile.append(users.id)
    
    for ids in username_profile:
        profile_list = Profile.objects.filter(id_user=ids)
        username_profile_list.append(profile_list)
    
    suggestions_username_profile_list=list(chain(*username_profile_list))
    comments=Comment.objects.all()
    posts=Post.objects.all()
    return render(request,'index.html',{'user_profile': user_profile,'posts': feedlists,'suggestions_username_profile_list':suggestions_username_profile_list[:4],'comments':comments})

@login_required(login_url='signin')
def upload(request):
    if request.method == 'POST':
        user=request.user.username
        image=request.FILES.get('image_upload')
        caption=request.POST['caption']

        new_post=Post.objects.create(user=user,image=image,caption=caption)
        new_post.save()
        return redirect('/')
    else:
        return redirect('/')
    
@login_required(login_url='signin')
def profile(request,pk):
    user_obj=User.objects.get(username=pk)
    user_profile=Profile.objects.get(user=user_obj)
    user_posts=Post.objects.filter(user=pk)
    user_posts_length=len(user_posts)

    follower=request.user.username
    user=pk

    if followersCount.objects.filter(follower=follower,user=user).first():
        button_text="Unfollow"
    else:
        button_text="Follow"

    user_followers=len(followersCount.objects.filter(user=pk))
    user_following=len(followersCount.objects.filter(follower=pk))

    context={
        'user_obj':user_obj,
        'user_profile':user_profile,
        'user_posts':user_posts,
        'user_post_length':user_posts_length,
        'button_text':button_text,
        'user_followers':user_followers,
        'user_following':user_following,
    }
    return render(request,"profile.html",context)

@login_required(login_url='signin')
def likePost(request):
    username=request.user.username
    post_id=request.GET.get('post_id')

    post=Post.objects.get(id=post_id)

    like_filter=like_post.objects.filter(post_id=post_id,username=username).first()
    if like_filter == None:
        new_like = like_post.objects.create(post_id=post_id,username=username)
        new_like.save()
        post.no_oflikes=post.no_oflikes+1
        post.save()
        return redirect('/')
    else:
        like_filter.delete()
        post.no_oflikes=post.no_oflikes-1
        post.save()
        return redirect('/')

@login_required(login_url='signin')
def comments(request):
    if request.method=='POST':
        username=request.user.username
        body=request.POST['comment']
        post_id=request.GET.get('post_id')
        print(post_id)
        post=Post.objects.get(id=post_id)
        post.no_ofcomments = post.no_ofcomments+1
        new_comment=Comment.objects.create(post=post_id,username=username,body=body)
        post.save()
        new_comment.save()
    return redirect('/')
   

@login_required(login_url='signin')
def follow(request):
    if request.method == 'POST':
        follower=request.POST['follower']
        user=request.POST['user']
        
        if followersCount.objects.filter(follower=follower,user=user).first():
            delete_follower=followersCount.objects.get(follower=follower,user=user)
            delete_follower.delete()
            return redirect('/profile/'+user)
        else:
            new_follower=followersCount.objects.create(follower=follower,user=user)
            new_follower.save() 
            return redirect('/profile/'+user)
    else:
        return redirect('/')

@login_required(login_url='signin')
def search(request):
    user_object=User.objects.get(username=request.user.username)
    user_profile=Profile.objects.get(user=user_object)

    if request.method == 'POST':
        username=request.POST['username']
        username_object=User.objects.filter(username__icontains=username)

        username_profile=[]
        username_profile_list=[]

        for users in username_object:
            username_profile.append(users.id)

        for ids in username_profile:
            profile_lists=Profile.objects.filter(id_user=ids)
            username_profile_list.append(profile_lists)

    username_profile_list=list(chain(*username_profile_list))

    return render(request,'search.html',{'user_profile': user_profile,'username_profile_list': username_profile_list})

@login_required(login_url='signin')
def settings(request):
    user_profile=Profile.objects.get(user=request.user)
    if request.method == 'POST':

        if request.FILES.get('image') != None:
            image = request.FILES.get('image')
            bio=request.POST['bio']
            location=request.POST['location']
            
            user_profile.profileimg=image
            user_profile.bio=bio
            user_profile.location=location
            user_profile.save()
        
        elif request.FILES.get('image') == None:
            image = user_profile.profileimg
            bio=request.POST['bio']
            location=request.POST['location']

            user_profile.profileimg=image
            user_profile.bio=bio
            user_profile.location=location
            user_profile.save()

        return redirect('/')
    return render(request,'setting.html',{'user_profile': user_profile})

def signup(request):
    if request.method == 'POST':
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        password2=request.POST['password2']

        if password==password2:
            if User.objects.filter(email=email).exists():
                messages.info(request,"Email already in use")
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request,"Username already in use")
                return redirect('signup')
            else:
                user= User.objects.create_user(username=username,email=email,password=password)
                user.save()

                #Log user in and redirect to settings page
                user_login= auth.authenticate(username=username,password=password)
                auth.login(request,user_login)

                #create a profile object for the new user
                user_model=User.objects.get(username=username)
                new_profile=Profile.objects.create(user=user_model,id_user=user_model.id)
                new_profile.save()
                return redirect('settings')
        else:
            messages.info(request,"Passwords not matching")
            return redirect('signup')
    else:        
        return render(request,'signup.html')
    
def signin(request):
    if request.method == 'POST':
        username=request.POST['username']
        password=request.POST['password']

        user=auth.authenticate(username=username,password=password)

        if user is not None:
            auth.login(request,user)
            return redirect('/')
        else:
            messages.info(request,"Credentials Invalid")
            return redirect('signin')
        
    else:
        return render(request,'signin.html')
    
@login_required(login_url='signin')
def logout(request):
    auth.logout(request)
    return redirect('signin')

