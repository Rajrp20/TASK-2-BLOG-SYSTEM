from django.shortcuts import render
from email.headerregistry import Group
from django import forms
from django.shortcuts import render,HttpResponseRedirect
from .forms import LoginForm,blogpostform
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from .models import blogpost
from django.contrib.auth.models import Group


def home(request):

    posts=blogpost.objects.all()
    return render(request,'blog/home.html',{'posts':posts})


def about(request):

    return render(request,'blog/about.html')


def contact(request):

    return render(request,'blog/contact.html')


def dashboard(request):

 if request.user.is_authenticated:
  posts=blogpost.objects.all()
  user=request.user
  full_name=user.get_full_name()
  gps=user.groups.all()
  return render(request,'blog/dashboard.html',{'posts':posts,'full_name':full_name,'groups':gps})
 else:
  return HttpResponseRedirect('/user_login/')

def user_logout(request):

    logout(request)
    return HttpResponseRedirect('/')




def user_login(request):

   if not request.user.is_authenticated:
    if request.method=="POST":
     form=LoginForm(request=request,data=request.POST)
     if form.is_valid():
       uname=form.cleaned_data['username']
       upass=form.cleaned_data['password']
       user=authenticate(username=uname,password=upass)
       if user is not None:
        login(request,user)
        messages.success(request,'Logged in Successfully !!!')
        return HttpResponseRedirect('/dashboard/')
    else:
     form=LoginForm()
    return render(request,'blog/login.html',{'form':form})  
    
   else:
    return HttpResponseRedirect('/dashboard/')



def add_post(request):

 if request.user.is_authenticated:
  if request.method=='POST':
   form=blogpostform(request.POST)
   if form.is_valid():
    title=form.cleaned_data['title']
    desc=form.cleaned_data['desc']
    pst=blogpost(title=title,desc=desc)
    pst.save()
    messages.success(request,'You have added the post')
    form=blogpostform()
  else:
   form=blogpostform()
  return render(request,'blog/addpost.html',{'form':form}) 
 else:
  return HttpResponseRedirect('/login/')

def update_post(request,id):
 
 if request.user.is_authenticated:
   if request.method=='POST':
     pi=blogpost.objects.get(pk=id)
     form=blogpostform(request.POST,instance=pi)
     if form.is_valid():
       form.save()
       messages.success(request,'You have Updated the post')
   else:
     pi=blogpost.objects.get(pk=id)
     form=blogpostform(instance=pi)

   return render(request,'blog/updatepost.html',{'form':form}) 
 else:
   return HttpResponseRedirect('/login/')

def delete_post(request,id):
 if request.user.is_authenticated:
   if request.method=='POST':
     pi=blogpost.objects.get(pk=id)
     pi.delete()

     return HttpResponseRedirect('/dashboard')
 else:
   return HttpResponseRedirect('/login/')
