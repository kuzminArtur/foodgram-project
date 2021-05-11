from django.urls import path

from . import views

urlpatterns = [
    path("", views.RecipesListView.as_view(), name='index'),
    ]