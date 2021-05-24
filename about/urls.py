from django.urls import path
from . import views

urlpatterns = [
    path('author/', views.author, name='author'),
    path('tech/', views.tech, name='tech'),
]
