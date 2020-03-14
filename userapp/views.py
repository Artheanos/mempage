from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseNotFound, Http404
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.core.serializers import serialize

from .utils import get_user, session_login, session_logout
from .forms import LoginForm, RegisterForm, EditForm
from .models import User


def login_form(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = User.objects.get(username=form.data['username'])
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
    if request.method == 'POST':
        user = get_user(request)
        form = EditForm(request.POST, instance=user)

        changed = (user.username, user.email) != (form.data['username'], form.data['email'])

        if form.is_valid():
            form.save()
            request.session['user'] = form.data['username']

            if changed:
                messages.add_message(request, messages.INFO, 'You have successfully edited your profile')
            return HttpResponseRedirect('/')
        else:
            return render(request, 'profile_edit_form.html', {'form': form})

    user = get_user(request)
    form = EditForm(instance=user)

    return render(request, 'profile_edit_form.html', {'form': form})


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
