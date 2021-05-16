from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, \
    PermissionRequiredMixin
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy

from .models import Recipe, Tag, Ingredient, RecipeIngredient
from .forms import RecipeForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView, \
    DeleteView

User = get_user_model()


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
    """Detail view for recipe."""
    template_name = 'recipes/recipe_detail.html'
    model = Recipe


def add_ingredients(post_data, recipe):
    """Create ingredients for recipe."""
    RecipeIngredient.objects.filter(recipe=recipe).delete()
    recipe_ingredients = []
    for key, value in post_data.items():
        if key.startswith('nameIngredient'):
            num = key.split('_')[1]
            ingredient = get_object_or_404(Ingredient, title=value)
            recipe_ingredients.append(
                RecipeIngredient(
                    recipe=recipe,
                    ingredient=ingredient,
                    amount=post_data[f'valueIngredient_{num}']
                )
            )
    RecipeIngredient.objects.bulk_create(recipe_ingredients)


class RecipeBaseNonSafeViewMixin:

    def form_valid(self, form):
        """Обработка валидных данных."""
        form.instance.author = self.request.user
        form.instance.save()
        add_ingredients(form.data, form.instance)
        return super().form_valid(form)

    def form_invalid(self, form):
        """Возврат сообщения об ошибке."""
        return super().render_to_response(
            self.get_context_data(form=form)
        )

    def has_permission(self):
        """Проверка является ли пользователь автором поста."""
        return self.request.user == get_object_or_404(
            User,
            recipe__slug=self.kwargs['slug']
        )

    def handle_no_permission(self):
        """Редирект при попытке редактирования не своего поста."""
        return redirect(reverse_lazy('recipe', kwargs=self.kwargs))

    def get_object(self, queryset=None):
        return get_object_or_404(Recipe, slug=self.kwargs['slug'])


class RecipeCreate(RecipeBaseNonSafeViewMixin, LoginRequiredMixin,
                   CreateView):
    """Create recipe."""
    form_class = RecipeForm
    template_name = 'recipes/recipe_form.html'

    def get_success_url(self):
        """Redirect to detail recipe view."""
        return reverse_lazy('recipe', kwargs={'slug': self.object.slug})


class RecipeDelete(RecipeBaseNonSafeViewMixin, LoginRequiredMixin, DeleteView):
    success_url = reverse_lazy('index')


class RecipeEdit(RecipeBaseNonSafeViewMixin, LoginRequiredMixin,
                 PermissionRequiredMixin, UpdateView):
    form_class = RecipeForm
    template_name = 'recipes/recipe_form.html'

    def get_success_url(self):
        """Redirect to detail recipe view."""
        return reverse_lazy('recipe', kwargs={'slug': self.object.slug})


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
