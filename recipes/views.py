from django.shortcuts import get_object_or_404, render, redirect
from .models import Recipe, Tag

from django.views.generic import ListView, DetailView


class BaseRecipesListView(ListView):
    model = Recipe
    paginate_by = 6


class IndexView(BaseRecipesListView):
    template_name = 'recipes/index.html'
    queryset = Recipe.objects.all().select_related('author')
    tags = Tag.objects.all()

    def get_context_data(self, **kwargs):
        """Add page title to the context."""
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
