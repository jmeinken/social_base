from datetime import datetime, timedelta

from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model

from . import forms

from pages.models import PageCategory


def home(request):
    context = {}
    context['qPageCategory'] = PageCategory.objects.all().filter(parent=None)
    return render(request, 'main/home.html', context)

@login_required
def home_private(request):
    context = {}
    return render(request, 'main/home.html', context)

def login_view(request):
    # if next is defined in the get request, we'll redirect there
    next = request.GET.get('next', False)
    # otherwise we'll redirect to the referring page
    if not next:
        next = request.META.get('HTTP_REFERER', 'home')
    # unless the referring page is the login page (will create infinite loop)
    if 'login' in next:
        next = 'home'
    if request.user.is_authenticated:
        return redirect(next)
    context = {}
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        # attempt to lookup user by email
        if user is None:
            User = get_user_model()
            qUser = User.objects.all().filter(email__iexact=username)
            if qUser:
                username = qUser[0].username
                user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                # redirect_to = request.POST.get(redirect_field_name, request.GET.get(redirect_field_name, ''))  
                return redirect(next)
            else:
                # Return a 'disabled account' error message
                context['login_error'] = 'Your account has a problem.  Please contact the administrator.'
                return render(request, 'main/login.html', context)
        else:
            # Return an 'invalid login' error message.
            context['login_error'] = 'Login failed.  Please reenter your username and password.'
            return render(request, 'main/login.html', context)
    return render(request, 'main/login.html', context)

@login_required
def logout_view(request):
    logout(request)
    # redirects back to the same page (for private systems, might want to redirect to the login page instead)
    next = request.META.get('HTTP_REFERER', 'home')
    return redirect(next)

def forgot_password(request):
    context = {}
    form = forms.ForgotPasswordForm()
    if request.POST:
        form = forms.ForgotPasswordForm(request.POST)
        if form.is_valid():
            # email forgot password
            form.email_forgot_password(request)
            messages.success(request, ''''You should soon receive an email with 
                instructions for resetting your password.  If you don't see it,
                check your spam folder.
            ''')
            return redirect('login')
    context['form'] = form
    return render(request, 'main/forgot_password.html', context)

def reset_password(request, temp_code):
    context = {}
    oUser = get_user_model().objects.all().get(temp_code=temp_code)
    thirty_days_ago = datetime.now() - timedelta(days=30)
    if oUser.temp_code_date.replace(tzinfo=None) < thirty_days_ago:
        messages.error(request, 'Your password reset code has expired.  Please request a new one.')
        return redirect('forgot_password')
    form = forms.PasswordForm(instance=oUser)
    if request.POST:
        form = forms.PasswordForm(request.POST, instance=oUser)
        if form.is_valid():
            oUser = form.save()
            messages.success(request, 'Password successfully changed.')
            user = authenticate(username=oUser.username, password=form.cleaned_data['password1'])
            login(request, user)
            return redirect('home')
    context['form'] = form
    return render(request, 'main/reset_password.html', context)

def create_account(request):
    context = {}
    form = forms.CreateAccountForm()
    if request.POST:
        form = forms.CreateAccountForm(request.POST)
        if form.is_valid():
            oUser = form.save()
            messages.success(request, 'Account successfully created.')
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
            login(request, user)
            return redirect('home')
    context['form'] = form
    return render(request, 'main/create_account.html', context)

@login_required
def account_settings(request):
    context = {}
    oUser = request.user
    form = forms.AccountEditForm(instance=oUser)
    password_form = forms.PasswordForm(instance=oUser)
    if request.POST:
        if 'account_form' in request.POST:
            form = forms.AccountEditForm(request.POST, instance=oUser)
            if form.is_valid():
                oUser = form.save()
                messages.success(request, 'Account successfully edited.')
                return redirect('home')
        if 'password_form' in request.POST:
            password_form = forms.PasswordForm(request.POST, instance=oUser)
            if password_form.is_valid():
                oUser = password_form.save()
                messages.success(request, 'Password successfully changed.')
                user = authenticate(username=request.user.username, password=password_form.cleaned_data['password1'])
                login(request, user)
                return redirect('home')
    context['form'] = form
    context['password_form'] = password_form
    return render(request, 'main/account_settings.html', context)














