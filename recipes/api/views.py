from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView

from .serializers import IngredientSerializer
from ..models import Ingredient


class GetIngredients(ListAPIView):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = [SearchFilter]
    search_fields = ['^title', ]
