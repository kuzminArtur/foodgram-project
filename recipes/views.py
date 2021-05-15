from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy

from .models import Recipe, Tag
from .forms import RecipeForm
from django.views.generic import ListView, DetailView, CreateView


class BaseRecipesListView(ListView):
    model = Recipe
    paginate_by = 6


class IndexView(BaseRecipesListView):
    template_name = 'recipes/index.html'
    queryset = Recipe.objects.all().select_related('author').prefetch_related(
        'tags')
    tags = Tag.objects.all()

    def get_context_data(self, **kwargs):
        """Add tags to the context."""
        kwargs.update({
            'tags': self.tags,
        })
        context = super().get_context_data(**kwargs)
        return context


class ProfileView(BaseRecipesListView):
    pass


class RecipeDetailView(DetailView):
    template_name = 'recipes/recipe_detail.html'
    model = Recipe


class RecipeCreate(LoginRequiredMixin, CreateView):
    form_class = RecipeForm
    uccess_url = reverse_lazy('index')
    template_name = 'recipes/recipe_create.html'
    tags = Tag.objects.all()

    # def get_context_data(self, **kwargs):
    #     """Add page title to the context."""
    #     kwargs.update({
    #         'tags': self.tags,
    #     })
    #     context = super().get_context_data(**kwargs)
    #     return context


class SubscriptionView(BaseRecipesListView):
    pass


class FavoriteView(DetailView):
    pass


def page_not_found(request, exception):
    """Отображает страницу 404 ошибки"""
    return render(
        request,
        "misc/404.html",
        {"path": request.path},
        status=404
    )


def server_error(request):
    """Отображает страницу 500 ошибки"""
    return render(request, "misc/500.html", status=500)
