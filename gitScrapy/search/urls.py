from django.urls import path
from .views import GetLogin


urlpatterns = [
    path('', GetLogin.as_view(), name='getLogin'),
]
