from django.shortcuts import render, HttpResponse,redirect
from home.models import Contact
from blog.models import Post
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
# Create your views here.
def home(request):
    allPosts = Post.objects.all()
    context = {'allPosts': allPosts}
    return render(request, 'home/home.html',context)


def about(request):
    return render(request, 'home/about.html')


def contact(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        content = request.POST['content']
        if len(name)<2 or len(email)<3 or len(phone)<10 or len(content)<4:
            messages.error(request,'Please fill your form properly')
        else:
            contact = Contact(name=name, email=email, phone=phone, content=content)
            contact.save()
            messages.success(request,'Your message has been succesfully sent')
         
    return render(request, 'home/contact.html')


def search(request):
    query = request.GET['query']
    if len(query)>78:
        allPosts = Post.objects.none()
    else:
        allPostsTitle = Post.objects.filter(title__icontains=query)
        allPostsContent = Post.objects.filter(content__icontains=query)
        allPosts = allPostsTitle.union(allPostsContent)
    if allPosts.count() == 0:
        messages.warning(request,'No search request found')
    params = {'allPosts':allPosts, 'query':query}
    return render(request,'home/search.html',params)


def handleSignup(request):
    if request.method == 'POST':
        #Get post parameters
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        #Check error inputs
        #username must be under 10 characters
        if len(username)>10:
            messages.error(request,"Username must be under 10 characters")
            return redirect('home')
        #username must be alphanumeric
        if not username.isalnum():
            messages.error(request,"Username must only contain letters and numbers")
            return redirect('home')
        #password must match
        if pass1 != pass2:
            messages.error(request,"Passwords don't match")
            return redirect('home')

        #Create the user
        myuser = User.objects.create_user(username,email,pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        messages.success(request,"Your iCoder account has been successfully created.")
        return redirect('home')
    else:
        return HttpResponse("Error!!404-not-found")


def handleLogin(request):
    if request.method == 'POST':
        #Get post parameters
        loginusername = request.POST['loginusername']
        loginpassword = request.POST['loginpassword']
        user = authenticate(username=loginusername, password=loginpassword)
        if user is not None:
            login(request,user)
            messages.success(request,"Succesfully logged in")
            return redirect('home')
        else:
            messages.error(request,"Invalid username and password")
            return redirect('home')

    return HttpResponse("Error!!404-not-found")


def handleLogout(request):
    logout(request)
    messages.success(request,"Succesfully logged out")
    return redirect('home')