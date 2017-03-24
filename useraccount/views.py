from django.contrib import auth
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from useraccount.forms import UserForm, LoginForm


def index(request):
    return render(request, 'index.html')


@csrf_exempt
def register(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        if user_form.is_valid():
            username = user_form.cleaned_data['username']
            password = user_form.cleaned_data['password']
            if User.objects.filter(username=username):
                return HttpResponse('<h3>registered</h3>')
            else:
                user = User.objects.create_user(username, None, password)
                user.is_superuser = True
                user.is_staff = True
                user.save()
                user = authenticate(username=username, password=password)
                auth.login(request, user)
                return render(request, 'index.html')
        else:
            return render(request, 'failure.html', {'reason': user_form.errors})
    else:
        user_form = UserForm()
    return render(request, 'register.html', {'form': user_form})

@csrf_exempt
def login(request):
    form = LoginForm()
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.isvalid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                auth.login(request, user)
                response = render(request, 'index.html', {'form': login_form})
                # username 写入cookie
                response.set_cookie('username', username, 3600)
                return response
            else:
                return render(request, 'login.html', {'form': form})
        else:
            return render(request, 'login.html', {'form': form})
    return render(request, 'login.html', {'form': form})

def logout(request):
    auth.logout(request)
    return render(request, 'index.html', locals())



