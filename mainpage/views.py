import datetime
import os
import boto3

from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render

from mempage.settings import IMAGES_DIR
from userapp.models import User
from .forms import UploadFileForm
from .models import Post, Comment
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


def main_page(request):
    page = request.GET.get('page')

    if page:
        try:
            page = int(page)
            page = max(1, page)
        except ValueError:
            return HttpResponseRedirect('/')
    else:
        page = 1

    posts_on_page = 50
    page -= 1

    posts = Post.objects.order_by('-date')[
            page * posts_on_page:
            (page + 1) * posts_on_page
            ]

    return render(request, 'main_page.html', {'posts': posts, 'session': request.session})


def post_page(request, post_number):
    post = Post.objects.get(pk=post_number)

    if request.method == 'POST':
        if not request.session.get('id'):
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


def post_edit_page(request, post_number):
    try:
        post = Post.objects.get(pk=post_number)
    except ObjectDoesNotExist:
        raise Http404(f"Post where id={post_number} does not exist")

    if request.method == 'POST':
        if post.user != User.get_user(request):
            raise Exception()

        if request.POST.get('action') == 'delete':
            remove_post(post)
        else:
            post.header = request.POST['new-header']
            post.save()

        return HttpResponseRedirect('/my_posts')

    return render(request, 'post_edit_page.html', {'post': post, 'session': request.session})


def my_posts_page(request):
    posts = Post.objects.filter(user=User.get_user(request))

    return render(request, 'my_posts_page.html', {'posts': posts, 'session': request.session})
