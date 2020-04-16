"""mempage URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from mainpage.views import main_page, upload_form, post_page, post_edit_page, my_posts_page
from userapp.views import login_form, register_form, logout, profile_edit_form, profile_page, password_recovery_page

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', main_page),
    path('post/<int:post_number>', post_page),
    path('post_edit/<int:post_number>', post_edit_page),
    path('upload', upload_form),
    path('logout', logout),

    path('login_form', login_form),
    path('register_form', register_form),
    path('profile_edit', profile_edit_form),
    path('profile_edit/password_change', profile_edit_form),
    path('my_posts', my_posts_page),

    path('password_recovery', password_recovery_page),

    path('profile/<int:profile_id>', profile_page),
]
