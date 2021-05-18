from rest_framework import status
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import IngredientSerializer
from ..models import Ingredient, Favorite


class GetIngredients(ListAPIView):
    """Searches for ingredients at the beginning of a word."""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = [SearchFilter]
    search_fields = ['^title', ]


class AddFavorites(APIView):
    """Add recipe to favorites."""

    def post(self, request, *args, **kwargs):
        Favorite.objects.get_or_create(
            user=request.user,
            recipe_id=request.data['id']
        )

        return Response({'success': True}, status=status.HTTP_200_OK)


class RemoveFavorites(APIView):
    """Delete recipe from favorites."""

    def delete(self, request, pk):
        Favorite.objects.filter(recipe_id=pk, user=request.user).delete()

        return Response({'success': True}, status=status.HTTP_200_OK)
