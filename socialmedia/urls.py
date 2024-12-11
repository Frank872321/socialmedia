"""
URL configuration for socialmedia project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path, include
from post.views import main, profiles
from user.views import Login, logout_view, register
from user.views import update_profile
from call.views import call
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', main, name="home"),
    path('profile/<str:user_id>', profiles, name="profile"),
    path('login/',Login.as_view(), name="login"),
    path('logout/', logout_view, name = 'Logout'),
    path('meet/', call, name="meet"),
    path('rooms/', include('ChitChat.urls')),
    path('register/', register, name="register"),
    path('update-profile/', update_profile, name='update_profile'),
]
if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)
