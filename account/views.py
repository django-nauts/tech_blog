from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from django.urls import reverse

from .forms import LoginForm
from .models import User


# Login View
def login_user(request):
    if request.method == 'GET':
        login_form = LoginForm()
        context = {
            'login_form': login_form
        }
        return render(request, 'account/login.html', context)


    elif request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_email = login_form.cleaned_data.get('email')
            user_pass = login_form.cleaned_data.get('password')
            user: User = User.objects.filter(email__iexact=user_email).first()
            if user is not None:
                if not user.is_active:
                    login_form.add_error('email', 'Your account is not active yet')
                else:
                    is_password_correct = user.check_password(user_pass)
                    if is_password_correct:
                        login(request, user)
                        return redirect('blog_index')
                    else:
                        login_form.add_error('email', 'Your password is wrong')
            else:
                login_form.add_error('email', 'Your account is not find')

        context = {
            'login_form': login_form
        }

        return render(request, 'account/login.html', context)


# Logout View
def logout_user(request):
        logout(request)
        return redirect(reverse('account:login_page'))