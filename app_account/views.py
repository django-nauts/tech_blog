from django.contrib.auth import login, logout
from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.crypto import get_random_string

from utils.email_service import send_email_to_user
from .forms import LoginForm, RegisterForm, ForgetPasswordForm, ResetPasswordForm
from .models import User


# Login View
def login_user(request):
    if request.method == 'GET':
        login_form = LoginForm()
        context = {
            'login_form': login_form
        }
        return render(request, 'app_account/login.html', context)


    elif request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_email = login_form.cleaned_data.get('email')
            user_pass = login_form.cleaned_data.get('password')
            user: User = User.objects.filter(email__iexact=user_email).first()
            if user is not None:
                if not user.is_active:
                    login_form.add_error('email', 'Your account is not active yet, please check your email')
                else:
                    is_password_correct = user.check_password(user_pass)
                    if is_password_correct:
                        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                        return redirect(reverse('blog_index'))
                    else:
                        login_form.add_error('email', 'Your password is wrong')
            else:
                login_form.add_error('email', 'Your account is not find')

        context = {
            'login_form': login_form
        }

        return render(request, 'app_account/login.html', context)


# Logout View
def logout_user(request):
    logout(request)
    return redirect('account:login_page')


def register_user(request):
    if request.method == 'GET':
        register_form = RegisterForm()
        context = {
            'register_form': register_form
        }
        return render(request, 'app_account/register.html', context)

    elif request.method == 'POST':
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_email = register_form.cleaned_data.get('email')
            user_password = register_form.cleaned_data.get('password')
            user: bool = User.objects.filter(email__iexact=user_email).exists()
            if user:
                register_form.add_error('email', 'your email is already registered')
            else:
                new_user = User(
                    email=user_email,
                    email_active_code=get_random_string(72),
                    is_active=False,
                    username=user_email)
                new_user.set_password(user_password)
                new_user.save()
                send_email_to_user('activate user account', new_user.email, {'user': new_user},
                                   'emails/activate_account.html')
                return redirect('app_account:login_page')

        context = {
            'register_form': register_form
        }

        return render(request, 'app_account/register.html', context)


def activate_user_account(request, email_active_code):
    if request.method == 'GET':
        user: User = User.objects.filter(email_active_code__iexact=email_active_code).first()
        if user is not None:
            if not user.is_active:
                user.is_active = True
                user.email_active_code = get_random_string(72)
                user.save()
                return redirect('app_account:login_page')
        raise Http404


def forget_password(request):
    if request.method == 'GET':
        forget_pass_form = ForgetPasswordForm()
        context = {
            'forget_pass_form': forget_pass_form
        }
        return render(request, 'app_account/forget_password.html', context)

    if request.method == 'POST':
        forget_pass_form = ForgetPasswordForm(request.POST)
        if forget_pass_form.is_valid():
            user_email = forget_pass_form.cleaned_data.get('email')
            user: User = User.objects.filter(email__iexact=user_email).first()
            if user is not None:
                send_email_to_user('Change password', user.email, {'user': user}, 'emails/forget_password.html')
                return redirect('blog_index')
        context = {
            'forget_pass_form': forget_pass_form
        }
        return render(request, 'app_account/forget_password.html', context)


def reset_password(request, email_active_code):
    if request.method == 'GET':
        user: User = User.objects.filter(email_active_code__iexact=email_active_code).first()
        if user is None:
            return redirect(reverse('app_account:login_page'))

        reset_pass_form = ResetPasswordForm()

        context = {
            'reset_pass_form': reset_pass_form,
            'user': user
        }
        return render(request, 'app_account/reset_password.html', context)

    if request.method == 'POST':
        reset_pass_form = ResetPasswordForm(request.POST)
        user: User = User.objects.filter(email_active_code__iexact=email_active_code).first()
        if reset_pass_form.is_valid():
            if user is None:
                return redirect('app_account:login_page')
            user_new_pass = reset_pass_form.cleaned_data.get('password')
            user.set_password(user_new_pass)
            user.email_active_code = get_random_string(72)
            user.is_active = True
            user.save()
            return redirect('app_account:login_page')

        context = {
            'reset_pass_form': reset_pass_form,
            'user': user
        }

        return render(request, 'app_account/reset_password.html', context)
