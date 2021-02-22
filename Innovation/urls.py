"""Innovation URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from Home import views as home_views
from User import views as user_views
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.conf import settings
from chat import views as chat_views

 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',home_views.home,name='Home'),
    path('register/',user_views.register,name='register'),
    path('log-in/',auth_views.LoginView.as_view(template_name='User/confirm_login.html'),name='login'),
    path('log-out/',auth_views.LogoutView.as_view(template_name='User/logout.html'),name='logout'),
    path('profile/<username>/',user_views.profile,name='profile'),
    path('update-profile/',user_views.update_profile,name='update-profile'),
    path('user-pics/<username>/',user_views.user_pics,name='user-pics'),
    path('user-pics/new',user_views.PostCreateView.as_view(),name='post-create'),
    path('like/<int:pk>',user_views.LikeView,name="like_profile"),
    path('chat/<username>/',chat_views.chat,name='chat'),
    path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        user_views.activate_account, name='activate'),
         path('message_query',chat_views.messages_db,name='messages_db'),
    path('notifications/',chat_views.notifications,name='notifications'),
    path('ajax',chat_views.ajax,name='ajax')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)