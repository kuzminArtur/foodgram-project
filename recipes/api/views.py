from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.http import JsonResponse
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from .serializers import IngredientSerializer
from ..models import Ingredient, Favorite, Follow, Purchase

User = get_user_model()

SUCCESS_RESPONSE = JsonResponse({'success': True})
FAIL_RESPONSE_DATA = JsonResponse(
    {'success': False},
    status=status.HTTP_400_BAD_REQUEST
)


class GetIngredients(ListAPIView):
    """Searches for ingredients at the beginning of a word."""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = [SearchFilter]
    search_fields = ['^title', ]


class AddRemoveBaseView(APIView):
    """Base view for create and delete."""
    permission_classes = [IsAuthenticated]
    model = None

    def post(self, request):
        """Create model instance."""
        try:
            self.model.objects.create(
                user=request.user,
                recipe_id=request.data['id']
            )
            return SUCCESS_RESPONSE

        except IntegrityError:
            return FAIL_RESPONSE_DATA

    def delete(self, request, pk):
        """Remove model instance."""
        count_deleted, _ = self.model.objects.filter(
            recipe_id=pk,
            user=request.user
        ).delete()

        if count_deleted:
            return SUCCESS_RESPONSE
        return FAIL_RESPONSE_DATA


class Favorites(AddRemoveBaseView):
    """Add/remove recipe to favorites."""
    model = Favorite


class Purchases(AddRemoveBaseView):
    """Add/remove recipe to purchases."""
    model = Purchase


class Subscriptions(APIView):
    """Add/remove user to author subscribers."""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        author = get_object_or_404(User, id=request.data['id'])

        try:
            self.validate_subscribe(author)

            Follow.objects.create(
                user=request.user,
                author=author
            )
            return SUCCESS_RESPONSE

        except(ValidationError, IntegrityError):
            return FAIL_RESPONSE_DATA

    def delete(self, request, pk):
        count_deleted, _ = Follow.objects.filter(
            author_id=pk,
            user=request.user
        ).delete()

        if count_deleted:
            return SUCCESS_RESPONSE
        return FAIL_RESPONSE_DATA

    def validate_subscribe(self, author):
        """Deny self-subscription."""
        if author == self.request.user:
            raise ValidationError
