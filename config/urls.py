"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from mainapp import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/',views.home_view,name='home_page'),
    path('qoshish/',views.qoshish,name='qoshish'),
    path('qidiruv/', views.qidiruv, name='qidiruv'),
    path('ochirish/<int:id>/', views.ochirish, name='ochirish'),
    path('tasdiqlash/<int:id>/', views.tasdiqlash, name='tasdiqlash'),
    path('yangilash/', views.yangilash, name='yangilash'),
    path('login/',views.login_view,name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.registry, name='signup'),
    path('',views.chiqaradi,name='landing'),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
