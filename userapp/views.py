from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render

from .forms import LoginForm, RegisterForm, EditProfileForm, ChangePasswordForm
from .models import User
from .utils import session_login, session_logout, session_logged_in


def login_form(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = User.objects.get(username=form.cleaned_data['username'])
            session_login(request, user)
            previous_page = request.POST.get('previous_page')
            print(previous_page)
            if previous_page:
                return HttpResponseRedirect(previous_page)
            return HttpResponseRedirect('/')
        else:
            return render(request, 'login_form.html', {'form': form})

    form = LoginForm()
    data = {'form': form}

    if request.GET.get('post'):
        data['previous_page'] = '/post/' + request.GET.get('post')

    return render(request, 'login_form.html', data)


def register_form(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            user = User.objects.get(username=form.data['username'])
            session_login(request, user)
            messages.add_message(request, messages.INFO, 'You have successfully registered')
            return HttpResponseRedirect('/')
        else:
            return render(request, 'register_form.html', {'form': form})

    form = RegisterForm()

    return render(request, 'register_form.html', {'form': form})


def profile_edit_form(request):
    if request.path.endswith('password_change'):
        if request.method == 'POST':  # change password request
            current_user = User.get_user(request)
            form = ChangePasswordForm(request.POST)
            if form.is_valid():
                if current_user.passwords_match(form.data['old_password']):
                    current_user.set_password(form.data['new_password'])
                    current_user.save()
                    messages.add_message(request, messages.INFO, 'Your password has been changed')
                else:
                    form.add_error('old_password', 'Password is incorrect')
                    return render(request, 'password_change_form.html', {'form': form})
            else:
                return render(request, 'password_change_form.html', {'form': form})

        #     if match(request.POST.get('old_password'), current_user.password):
        #         new_password = request.POST.get('new_password')
        #         current_user.password = encrypt(new_password)
        #         current_user.save()
        #
        #         messages.add_message(request, messages.INFO, 'Your password has been changed')
        #         return render(request, 'password_change_form.html')
        #
        #     messages.add_message(request, messages.INFO, 'Bad password')
        #     return render(request, 'password_change_form.html')

        form = ChangePasswordForm()
        return render(request, 'password_change_form.html', {'form': form})

    else:

        if request.method == 'POST':  # edit profile request
            user = User.get_user(request)
            form = EditProfileForm(request.POST, instance=user)

            changed = (user.username, user.email) != (form.data['username'], form.data['email'])

            if form.is_valid():
                form.save()
                request.session['username'] = form.data['username']

                if changed:
                    messages.add_message(request, messages.INFO, 'You have successfully edited your profile')
                return HttpResponseRedirect('/')
            else:
                return render(request, 'profile_edit_form.html', {'form': form})

        user = User.get_user(request)
        form = EditProfileForm(instance=user)

        return render(request, 'profile_edit_form.html', {'form': form})


def password_recovery_page(request):
    if request.method == 'POST':
        target_email = request.POST.get('target_email')
        if target_email:
            target_user = User.objects.get(email=target_email)
            target_user.forgot_password()

        return render(request, 'password_recovery/second_stage.html')

    if session_logged_in(request):
        return render(request, 'password_recovery/first_stage.html', {'target_email': User.get_user(request).email})
    else:
        return render(request, 'password_recovery/first_stage.html')


def profile_page(request, profile_id):
    try:
        user = User.objects.get(id=profile_id)
        stats = {
            'Number of posts': user.post_set.count(),
            'Number of comments': user.comment_set.count()
        }
        return render(request, 'profile_page.html', {'user': user, 'stats': stats, 'session': request.session})
    except ObjectDoesNotExist:
        raise Http404("User does not exist")


def logout(request, goto_page=None):
    session_logout(request)
    return HttpResponseRedirect(goto_page if goto_page else '/')
