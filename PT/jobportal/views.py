from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import Profile
from django.contrib.auth.decorators import login_required

@login_required(login_url='signin')
def base(request):
    return render(request, 'jobportal/base.html')

def signup(request):
    if request.method == 'POST':
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 == password2:
            if User.objects.filter(email=email).exists():
                messages.error(request, 'Email is already taken')
                return redirect('signup')
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username is already taken')
                return redirect('signup')
            else:
                user = User.objects.create_user(
                    first_name=fname, last_name=lname, username=username, password=password1, email=email)
                user.save()

                user_login = auth.authenticate(username=username, password=password1)
                if user_login is not None:
                    auth.login(request, user_login)

                    user_model = User.objects.get(username=username)
                    new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
                    new_profile.save()
                    return redirect('/')
                else:
                    messages.error(request, 'Authentication failed')
                    return redirect('signin')
        else:
            messages.error(request, 'Passwords do not match')
            return redirect('signup')

    return render(request, 'jobportal/signup.html')

def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request,user)
            return redirect('/')
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('signin')
    else:
        return render(request, 'jobportal/signin.html')
@login_required(login_url='signin')
def logout(request):
    auth.logout(request)
    return redirect('signin')