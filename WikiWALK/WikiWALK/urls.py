"""WikiWALK URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path, re_path
from . import view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('Game', view.newGame, name='Game'),
    path('', view.startGame, name='Home'),
    path('aboutUs',view.aboutus_page, name='About'),
    path('howtoplay',view.play_page, name='Play'),
    # path('India', view.nextLink, name='India')
    re_path(r'^forwards/(?P<next_link>.+?)/$', view.nextLink, name='forwards')
]
