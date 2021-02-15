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
from django.views.generic import UpdateView

from mainpage.views import upload_form, post_page, MainView, MyPostsView, MyPostEditView, \
    MyPostDeleteView
from userapp.views import login_form, register_form, logout, profile_edit_form, profile_page, password_recovery_page

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', MainView.as_view(), name='main-page'),
    path('my_posts', MyPostsView.as_view(), name='my-posts'),
    path('post/<int:pk>', post_page, name='post-page'),
    path('post/<int:pk>/edit', MyPostEditView.as_view(), name='post-edit'),
    path('post/<int:pk>/delete', MyPostDeleteView.as_view(), name='post-delete'),
    path('upload', upload_form, name='upload'),
    path('logout', logout, name='logout'),

    path('login_form', login_form, name='login'),
    path('register_form', register_form, name='register'),
    path('profile_edit', profile_edit_form, name='profile-edit'),
    path('profile_edit/password_change', profile_edit_form, name='password-change'),

    path('password_recovery', password_recovery_page, name='password-recovery'),

    path('profile/<int:pk>', profile_page, name='profile-page'),
]
