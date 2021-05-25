from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns

from . import views
from .api import views as api_views

views_patterns = [
    path("", views.IndexView.as_view(), name='index'),
    path('recipes/<slug:slug>/', views.RecipeDetailView.as_view(),
         name='recipe'),
    path('recipes/<slug:slug>/edit/', views.RecipeEdit.as_view(),
         name='edit'),
    path('recipes/<slug:slug>/delete/', views.RecipeDelete.as_view(),
         name='delete'),
    path('new/', views.RecipeCreate.as_view(), name='new'),
    path('profiles/<str:username>/', views.ProfileView.as_view(),
         name='profile'),
    path('subscriptions/', views.SubscriptionView.as_view(),
         name='subscription'),
    path('favorites/', views.FavoriteView.as_view(), name='favorite'),
    path('purchases/', views.PurchasesView.as_view(), name='purchases'),
    path('download/', views.download, name='download'),

]

api_patterns = [
    path('ingredients/', api_views.GetIngredients.as_view(),
         name='ingredient'),
    path('favorites/', api_views.Favorites.as_view()),
    path('favorites/<int:pk>/', api_views.Favorites.as_view()),
    path('subscriptions/', api_views.Subscriptions.as_view()),
    path('subscriptions/<int:pk>/', api_views.Subscriptions.as_view()),
    path('purchases/', api_views.Purchases.as_view()),
    path('purchases/<int:pk>/', api_views.Purchases.as_view(),
         name='remove_purchase'),
]

urlpatterns = [
    path('', include(views_patterns)),
    path('api/', include(format_suffix_patterns(api_patterns))),
]
