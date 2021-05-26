from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)
from django.db.models import Sum, F
from django.http import FileResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import (ListView, DetailView, CreateView, UpdateView,
                                  DeleteView)

from .forms import RecipeForm
from .mixins import IsInPurchasesMixin, IsFavoriteMixin
from .models import Recipe, Tag, Follow
from .utils import get_pdf, add_ingredients

User = get_user_model()

OBJECTS_PER_PAGE = 6


class BaseRecipesListView(IsInPurchasesMixin, IsFavoriteMixin, ListView):
    """Base class for recipe list."""
    model = Recipe
    paginate_by = OBJECTS_PER_PAGE
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
        """Filter by tags."""
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


class RecipeBaseNonSafeViewMixin(LoginRequiredMixin):
    """Common methods for Recipe create/edit/delete view."""

    form_class = RecipeForm
    template_name = 'recipes/recipe_form.html'

    def get_success_url(self):
        """Redirect to detail recipe view."""
        return self.success_url or reverse_lazy(
            'recipe',
            kwargs={'slug': self.object.slug}
        )

    def form_valid(self, form):
        """Processing valid data."""
        form.instance.author_id = (form.instance.author_id or
                                   self.request.user.id)
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


class RecipeDelete(RecipeBaseNonSafeViewMixin, DeleteView):
    """Delete recipe view."""
    template_name = None
    success_url = reverse_lazy('index')


class RecipeEdit(RecipeBaseNonSafeViewMixin,
                 PermissionRequiredMixin, UpdateView):
    """Edit an existing recipe."""


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
    paginate_by = OBJECTS_PER_PAGE
    queryset = User.objects.all()
    template_name = 'recipes/subscriptions.html'

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(following__user=self.request.user).prefetch_related(
            'recipes')

        return qs


class PurchasesView(LoginRequiredMixin, ListView):
    """Show recipes in purchases."""
    page_title = 'Избранное'
    template_name = 'recipes/purchases.html'

    def get_queryset(self):
        """Display recipes in purchases."""
        qs = self.request.user.purchases.all()

        return qs


@login_required
def download(request):
    """Upload pdf-file with purchases ingredients."""
    purchases = request.user.purchases.select_related('recipe').annotate(
        title=F('recipe__ingredients__title'),
        unit=F('recipe__ingredients__unit')
    ).values(
        'title', 'unit'
    ).annotate(
        amount=Sum('recipe__recipe_ingredient__amount')
    )
    buffer = get_pdf(purchases)
    return FileResponse(buffer, as_attachment=True, filename='need_to_by.pdf')
