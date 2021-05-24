from django.db.models import Exists, OuterRef

from recipes.models import Favorite, Purchase


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
