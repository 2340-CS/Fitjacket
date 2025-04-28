from django.shortcuts import render
from django.conf import settings
# Create your views here.
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from django.shortcuts import redirect
from .forms import CustomUserCreationForm, CustomErrorList
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import FitUser

def signup(request):
    template_data = {}
    template_data['title'] = 'Sign Up'
    if request.method == 'GET':
        template_data['form'] = CustomUserCreationForm()
        return render(request, 'accounts/signup.html', {'template_data': template_data})
    elif request.method == 'POST':
        form = CustomUserCreationForm(request.POST, error_class = CustomErrorList)
        if form.is_valid():
            form.save()
            return redirect('login')
        else:
            template_data['form'] = form
            return render(request, 'accounts/signup.html', {'template_data': template_data})
        
@login_required
def logout(request):
    auth_logout(request)
    return redirect('home')

def login(request):
    template_data = {}
    template_data['title'] = 'Login'
    if request.method == 'GET':
        return render(request, 'accounts/login.html', {'template_data': template_data})
    elif request.method == 'POST':
        user = authenticate(
            request,
            username = request.POST['username'],
            password = request.POST['password']
        )
        if user is None:
            template_data['error'] = 'The username or password is incorrect.'
            return render(request, 'accounts/login.html', {'template_data': template_data})
        else:
            auth_login(request, user)
            return redirect('home')


def account_view(request, *args, **kwargs):
    user_id = kwargs.get('user_id')
    profile_user = get_object_or_404(FitUser, id=user_id)

    is_self = False
    hide_email = False

    if request.user.is_authenticated:
        if request.user.id == profile_user.id:
            is_self = True
            if request.method == 'POST':
                new_interests = request.POST.getlist('interests')
                profile_user.interests = new_interests
                profile_user.save()
                return redirect('accounts:view', user_id=user_id)
        else:
            if not profile_user.email:
                hide_email = True
    else:
        hide_email = True

    context = {
        'username': profile_user.username,
        'email': profile_user.email,
        'bio': profile_user.bio,
        'profile_picture': profile_user.profile_picture,
        'interests': profile_user.interests,
        'is_self': is_self,
        'hide_email': hide_email,
    }

    return render(request, 'accounts/account.html', context)