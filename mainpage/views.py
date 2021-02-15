import datetime
import os
import boto3

from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import QuerySet
from django.forms import ModelForm
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, View, UpdateView, DeleteView
from django.views.generic.base import ContextMixin
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.list import MultipleObjectMixin

from mempage.settings import IMAGES_DIR
from userapp.models import User
from userapp.utils import session_logged_in
from .forms import UploadFileForm
from .models import Post, Comment, PostForm
from .utils import is_image, name_save_file, remove_post

S3 = boto3.client('s3')
S3_BUCKET = 'mempagebucket'


def upload_form(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file_name = name_save_file(request.FILES['file'])
            file_path = os.path.join(IMAGES_DIR, file_name)

            if not is_image(file_path):
                os.remove(file_path)

                messages.add_message(request, messages.INFO, 'File is not an image')
                formset = UploadFileForm(request.POST)
                return render(
                    request, 'upload_form.html', {'formset': formset, 'session': request.session}
                )

            S3.upload_file(file_path, S3_BUCKET, 'media/' + file_name)

            new_post = Post.objects.new_post(request.POST['header'], file_name, User.get_user(request))
            new_post.save()

            messages.add_message(request, messages.INFO, 'You have successfully uploaded an image')
            return HttpResponseRedirect('/')
        else:
            return HttpResponse('Form is not valid')

    else:
        formset = UploadFileForm(request.POST)
        return render(
            request, 'upload_form.html', {'formset': formset, 'session': request.session}
        )


def post_page(request, pk):
    post = Post.objects.get(pk=pk)

    if request.method == 'POST':
        if not session_logged_in(request):
            return HttpResponseRedirect('/')

        if request.POST.get('comment-id'):
            comment = Comment.objects.get(pk=request.POST['comment-id'])
            comment.delete()
            return HttpResponseRedirect(request.path_info)
        else:
            comment = Comment.objects.create(
                user=User.get_user(request),
                post=post,
                date=datetime.datetime.now(),
                content=request.POST['content']
            )
            comment.save()
            return HttpResponseRedirect(request.path_info)

    return render(request, 'post_page.html', {'post': post, 'session': request.session})


class SessionContext(ContextMixin, View):
    def get_context_data(self, *, object_list=None, **kwargs):
        return super().get_context_data(
            object_list=object_list, **kwargs,
            session=self.request.session
        )


class MainView(SessionContext, ListView):
    model = Post
    template_name = 'main_page.html'
    ordering = ['-date']
    paginate_by = 10

    # def get_context_data(self, *, object_list=None, **kwargs):
    #     queryset: QuerySet = object_list if object_list is not None else self.object_list


class MyPostsView(MainView):
    template_name = 'my_posts_page.html'

    def get_queryset(self):
        return super().get_queryset().filter(user=User.get_user(self.request))


class OwnerOnly(SingleObjectMixin, View):
    def get_object(self, queryset=None):
        post = super().get_object(queryset)
        if post.user.id != self.request.session['id']:
            raise Http404('You are not the owner')
        return post


class MyPostEditView(SessionContext, OwnerOnly, UpdateView):
    model = Post
    form_class = PostForm
    success_url = '/my_posts'


class MyPostDeleteView(SessionContext, OwnerOnly, DeleteView):
    model = Post
    success_url = reverse_lazy('main-page')
