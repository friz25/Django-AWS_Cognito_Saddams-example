from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('sign-out', views.signout, name='signout'),
]