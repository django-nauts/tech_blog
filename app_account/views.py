from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import Http404, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.crypto import get_random_string

from utils.email_service import send_email_to_user
from .forms import LoginForm, RegisterForm, ForgetPasswordForm, ResetPasswordForm, EditProfileModelForm, \
    ChangePasswordForm
from .models import User, Contact
from blog.models import Post


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
                        messages.success(request, f'Welcome back, { user }!')
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
                messages.success(request, 'Your password was updated successfully!')
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


def user_dashboard(request, pk):
    user_page = User.objects.get(id=pk)
    posts = Post.objects.filter(author=user_page).order_by('-created')
    paginator = Paginator(posts, 1)
    page_number = request.GET.get("page")

    # Display the last result instead of non-existing page.
    try:
        page_obj = paginator.get_page(page_number)
    except EmptyPage:
        page_obj = paginator.get_page(paginator.num_pages)

    # Display the first page in the page number is a character.
    except PageNotAnInteger:
        page_obj = paginator.page(1)

    context = {
        'user_page': user_page,
        'posts': posts,
        'page_obj': page_obj,
    }
    return render(request, 'app_account/user_dashboard.html', context)


def user_dashboard_sidebar_component(request):
    return render(request, 'app_account/component/user_dashboard_sidebar.html')


#
def user_edit_profile(request):
    current_user = User.objects.filter(id=request.user.id).first()

    if request.method == 'GET':
        edit_profile_form = EditProfileModelForm(instance=current_user)
        context = {
            'edit_profile_form': edit_profile_form,
            'current_user': current_user,
        }
        return render(request, 'app_account/user_edit_profile.html', context)

    if request.method == 'POST':
        edit_profile_form = EditProfileModelForm(data=request.POST, instance=current_user, files=request.FILES)
        if edit_profile_form.is_valid():
            edit_profile_form.save()
        context = {
            'edit_profile_form': edit_profile_form,
            'current_user': current_user,
        }
        return render(request, 'app_account/user_edit_profile.html', context)


def user_change_password(request):
    if request.method == 'GET':
        current_user: User = User.objects.filter(id=request.user.id).first()
        change_pass_form = ChangePasswordForm()
        context = {
            'change_pass_form': change_pass_form,
            'current_user': current_user,
        }
        return render(request, 'app_account/user_change_password.html', context)

    if request.method == 'POST':
        change_pass_form = ChangePasswordForm(request.POST)
        if change_pass_form.is_valid():
            current_user: User = User.objects.filter(id=request.user.id).first()
            if current_user.check_password(change_pass_form.cleaned_data.get('current_password')):
                current_user.set_password(change_pass_form.cleaned_data.get('new_password'))
                current_user.save()
                logout(request)
                return redirect('account:login_page')
            else:
                change_pass_form.add_error('current_password', 'Your password is wrong')

        context = {
            'change_pass_form': change_pass_form,
        }
        return render(request, 'app_account/user_change_password.html', context)


@login_required
def user_list(request):
    users = User.objects.filter(is_active=True)
    return render(request, 'app_account/user_list.html', {'users': users})

# Follow or unfollow a user
@login_required
def user_follow(request):
    if request.POST.get('action') == 'post':
        user_id = request.POST.get('userid')
        action = request.POST.get('followAction')
        print("=======================================================")
        print(user_id)
        print(action)
        print("=======================================================")
        if user_id and action:
            try:
                user = User.objects.get(id=user_id)
                if action == 'follow':
                    Contact.objects.get_or_create(user_from=request.user, user_to=user)
                else:
                    Contact.objects.filter(user_from=request.user, user_to=user).delete()
                return JsonResponse({'status': 'ok'})
            except User.DoesNotExist:
                return JsonResponse({'status': 'error'})
        return JsonResponse({'status': 'error'})
