from django.urls import path

from . import views

urlpatterns = [
    path("", views.IndexView.as_view(), name='index'),
    path('recipes/<slug:slug>', views.RecipeDetailView.as_view(),
         name='recipe'),
    path('profiles/<str:username>/', views.ProfileView.as_view(),
         name='profile'),
    path('subscriptions/', views.SubscriptionView.as_view(),
         name='subscription'),
    path('favorites/', views.FavoriteView.as_view(), name='favorite'),
    path('new/', views.RecipeCreate.as_view(), name='new'),

]
