from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import IngredientSerializer
from ..models import Ingredient, Favorite, Follow, Purchase

User = get_user_model()


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
        self.model.objects.get_or_create(
            user=request.user,
            recipe_id=request.data['id']
        )

        return Response({'success': True}, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        """Remove model instance."""
        self.model.objects.filter(recipe_id=pk, user=request.user).delete()

        return Response({'success': True}, status=status.HTTP_200_OK)


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

        if not self.validate_subscribe(author):
            return Response(
                {'success': False},
                status=status.HTTP_403_FORBIDDEN
            )

        Follow.objects.get_or_create(
            user=request.user,
            author=author
        )

        return Response({'success': True}, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        Follow.objects.filter(author_id=pk, user=request.user).delete()

        return Response({'success': True}, status=status.HTTP_200_OK)

    def validate_subscribe(self, author):
        """Deny self-subscription."""
        return author != self.request.user
