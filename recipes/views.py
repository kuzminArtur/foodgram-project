from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, \
    PermissionRequiredMixin
from django.db.models import Exists, OuterRef
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy

from .models import Recipe, Tag, Ingredient, RecipeIngredient, Favorite
from .forms import RecipeForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView, \
    DeleteView

User = get_user_model()


class IsFavoriteMixin:
    """Add annotation with favorite mark to the View."""

    def get_queryset(self):
        """Annotate with favorite mark."""
        qs = super().get_queryset()
        qs = (
            qs.select_related('author').annotate(
                is_favorite=Exists(
                    Favorite.objects.filter(
                        user_id=self.request.user.id,
                        recipe_id=OuterRef('pk'),
                    ),
                )
            )
        )

        return qs


class BaseRecipesListView(IsFavoriteMixin, ListView):
    model = Recipe
    paginate_by = 6
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


class IndexView(BaseRecipesListView):
    """Main page with recipes list."""
    template_name = 'recipes/index.html'


class ProfileView(BaseRecipesListView):
    template_name = 'recipes/profile.html'

    def get(self, request, *args, **kwargs):
        """Store `author` parameter for data filtration purposes."""
        self.author = get_object_or_404(User, username=kwargs.get('username'))

        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        """Filer recipes by author."""
        qs = super().get_queryset()
        qs = qs.filter(author=self.author)

        return qs

    def get_context_data(self, **kwargs):
        kwargs.update({
            'author': self.author,
        })
        context = super().get_context_data(**kwargs)
        return context


class RecipeDetailView(IsFavoriteMixin,DetailView):
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
    """Common methods for Recipe create/edit/delete view."""

    def form_valid(self, form):
        """Обработка валидных данных."""
        form.instance.author = self.request.user
        form.instance.save()
        add_ingredients(form.data, form.instance)
        return super().form_valid(form)

    def form_invalid(self, form):
        """Return error message."""
        return super().render_to_response(
            self.get_context_data(form=form)
        )

    def has_permission(self):
        """Check recipe owner."""
        return self.request.user == get_object_or_404(
            User,
            recipe__slug=self.kwargs['slug']
        ) or self.request.user.is_superuser

    def handle_no_permission(self):
        """Redirection in case of an attempt to edit someone else's recipe."""
        return redirect(reverse_lazy('recipe', kwargs=self.kwargs))

    def get_object(self):
        """Get edited recipe object."""
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
    """Delete recipe view."""
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
