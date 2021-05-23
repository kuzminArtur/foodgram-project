from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, \
    PermissionRequiredMixin
from django.db.models import Exists, OuterRef
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy

from .models import Recipe, Tag, Ingredient, RecipeIngredient, Favorite, \
    Follow, Purchase
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
            qs.annotate(
                is_favorite=Exists(
                    Favorite.objects.filter(
                        user_id=self.request.user.id,
                        recipe_id=OuterRef('pk')
                    ),
                )
            )
        )
        return qs


class IsInPurchasesMixin:
    """Add annotation with purchases mark to the View."""

    def get_queryset(self):
        """Annotate with favorite mark."""
        qs = super().get_queryset()
        qs = (
            qs.annotate(
                is_in_purchases=Exists(
                    Purchase.objects.filter(
                        user_id=self.request.user.id,
                        recipe_id=OuterRef('pk')
                    ),
                )
            )
        )
        return qs


class BaseRecipesListView(IsInPurchasesMixin, IsFavoriteMixin, ListView):
    """Base class for recipe list."""
    model = Recipe
    paginate_by = 6
    queryset = Recipe.objects.all().select_related(
        'author').prefetch_related(
        'tags')
    tags = Tag.objects.all()
    page_title = None

    def get_context_data(self, **kwargs):
        """Add tags to the context."""
        kwargs.update({
            'tags': self.tags,
            'page_title': self._get_page_title()
        })
        context = super().get_context_data(**kwargs)
        return context

    def _get_page_title(self):
        """Get page title."""
        assert self.page_title, f"Attribute 'page_title' not set for {self.__class__.__name__}"  # noqa

        return self.page_title

    def get_queryset(self):
        filter_tag = self.request.GET.getlist('filter_tag')
        qs = super().get_queryset()
        if filter_tag:
            qs = qs.filter(tags__slug__in=filter_tag).distinct()
        return qs


class IndexView(BaseRecipesListView):
    """Main page with recipes list."""
    template_name = 'recipes/index.html'
    page_title = 'Рецепты'


class ProfileView(BaseRecipesListView):
    """Show only recipes by a specific author."""
    template_name = 'recipes/profile.html'
    page_title = 'Рецепты'

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
        """Add author to the context."""
        is_subscriber = (
                self.request.user.is_authenticated and
                Follow.objects.filter(
                    author=self.author,
                    user=self.request.user
                ).exists()
        )
        kwargs.update({
            'author': self.author,
            'is_subscriber': is_subscriber,
        })
        context = super().get_context_data(**kwargs)
        return context


class RecipeDetailView(IsInPurchasesMixin, IsFavoriteMixin, DetailView):
    """Detail view of the recipe."""
    template_name = 'recipes/recipe_detail.html'
    model = Recipe
    queryset = Recipe.objects.all()

    def get_queryset(self):
        """Annotate with favorite mark."""
        qs = super().get_queryset()
        qs = qs.select_related('author').prefetch_related(
            'recipe_ingredient__ingredient').prefetch_related('tags')
        return qs

    def get_context_data(self, **kwargs):
        """Add subscriber mark to the context."""
        is_subscriber = (
                self.request.user.is_authenticated and
                Follow.objects.filter(
                    author=self.object.author,
                    user=self.request.user
                ).exists()
        )
        kwargs.update({
            'is_subscriber': is_subscriber,
        })
        context = super().get_context_data(**kwargs)
        return context


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


class RecipeBaseNonSafeViewMixin(LoginRequiredMixin):
    """Common methods for Recipe create/edit/delete view."""

    def form_valid(self, form):
        """Processing valid data."""
        form.instance.author = form.instance.author or self.request.user
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
            recipes__slug=self.kwargs['slug']
        ) or self.request.user.is_superuser

    def handle_no_permission(self):
        """Redirection in case of an attempt to edit someone else's recipe."""
        return redirect(reverse_lazy('recipe', kwargs=self.kwargs))

    def get_object(self):
        """Get edited recipe object."""
        return get_object_or_404(Recipe, slug=self.kwargs['slug'])


class RecipeCreate(RecipeBaseNonSafeViewMixin,
                   CreateView):
    """Create recipe."""
    form_class = RecipeForm
    template_name = 'recipes/recipe_form.html'

    def get_success_url(self):
        """Redirect to detail recipe view."""
        return reverse_lazy('recipe', kwargs={'slug': self.object.slug})


class RecipeDelete(RecipeBaseNonSafeViewMixin, DeleteView):
    """Delete recipe view."""
    success_url = reverse_lazy('index')


class RecipeEdit(RecipeBaseNonSafeViewMixin,
                 PermissionRequiredMixin, UpdateView):
    """Edit an existing recipe."""
    form_class = RecipeForm
    template_name = 'recipes/recipe_form.html'

    def get_success_url(self):
        """Redirect to detail recipe view."""
        return reverse_lazy('recipe', kwargs={'slug': self.object.slug})


class FavoriteView(LoginRequiredMixin, BaseRecipesListView):
    """Show only favorite recipes."""
    page_title = 'Избранное'
    template_name = 'recipes/index.html'

    def get_queryset(self):
        """Display favorite recipes only."""
        qs = super().get_queryset()
        qs = qs.filter(fancier__user=self.request.user)

        return qs


class SubscriptionView(LoginRequiredMixin, ListView):
    """Show only subscription authors."""
    model = User
    paginate_by = 6
    queryset = User.objects.all()
    template_name = 'recipes/subscriptions.html'

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(following__user=self.request.user).prefetch_related(
            'recipes')

        return qs


class PurchasesView(LoginRequiredMixin, BaseRecipesListView):
    """Show recipes in purchases."""
    page_title = 'Избранное'
    template_name = 'recipes/index.html'

    def get_queryset(self):
        """Display favorite recipes only."""
        qs = super().get_queryset()
        qs = qs.filter(purchases__user=self.request.user)

        return qs


def page_not_found(request, exception):
    """Show 404 error page."""
    return render(
        request,
        "misc/404.html",
        {"path": request.path},
        status=404
    )


def server_error(request):
    """Show 505 error page."""
    return render(request, "misc/500.html", status=500)
