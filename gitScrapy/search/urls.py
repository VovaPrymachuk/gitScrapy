from django.urls import path
from . import views


urlpatterns = [
    path('', views.getLogin, name='getLogin'),
    path('result', views.getLogin, name='getLogin'),
]