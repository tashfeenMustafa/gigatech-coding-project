from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import Post

# Create your views here.
def index(request):
    posts = Post.objects.all()
    return render(request, 'index.html', {'posts': posts})

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email Already Used')
                return redirect('register')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username Taken')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save(); 
                return redirect('login')
        else:
            messages.info(request, 'Passwords do not match')
            return redirect('register')
    else:
        return render(request, 'register.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Credentials Invalid')
            return redirect('login')
    else:
        return render(request, 'login.html')

def logout(request):
    auth.logout(request)
    return redirect('/')

def createpost(request):
    return render(request, 'createpost.html')

def submitpost(request):
    if request.method == 'POST':
        title = request.POST['title']
        body = request.POST['body']

        if not title == '' or not body == '':
            post = Post.objects.create(title=title, body=body)
            post.save(); 
            return redirect('/')
        else: 
            messages.info(request, 'No title or body added')
            return redirect('createpost')

def post(request, pk):
    return render(request, 'post.html', {'pk': pk})