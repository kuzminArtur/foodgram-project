from django.shortcuts import get_object_or_404, render, redirect
from .models import Recipe

# def index(request):
#     return render(request, 'recipes/index.html')
from django.views.generic import ListView


class RecipesListView(ListView):
    model = Recipe
    paginate_by = 6
    template_name = 'recipes/index.html'
    queryset = Recipe.objects.all()  # .select_related('author__username')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


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
