import os
from random import choice
from string import ascii_lowercase, ascii_uppercase

from django.db.models import Model
from django.core.files.uploadedfile import InMemoryUploadedFile

from .models import Post
from mempage.settings import IMAGES_DIR


def random_string(length: int):
    pool = ascii_lowercase + ascii_uppercase + "-_~!$&'()+,;=@"
    return ''.join([choice(pool) for _ in range(length)])


def name_save_file(file: InMemoryUploadedFile) -> str:
    """
    Saves a file using a random name and returns the name
    """
    file_extension = file.name.split('.')[-1]
    target_file_name = '.' + file_extension
    target_file_name = random_string(20 - len(target_file_name)) + target_file_name
    with open(
            os.path.join(IMAGES_DIR, target_file_name),
            'wb+'
    ) as destination:
        for chunk in file.chunks():
            destination.write(chunk)

    return target_file_name


def remove_post(post: Post):
    os.rename(
        os.path.join(IMAGES_DIR, post.image),
        os.path.join(IMAGES_DIR, 'removed', post.image)
    )
    post.delete()
