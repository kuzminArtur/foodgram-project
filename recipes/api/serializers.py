from rest_framework import serializers

from ..models import Ingredient


class IngredientSerializer(serializers.ModelSerializer):
    """Rename field unit to dimension."""
    dimension = serializers.CharField(source='unit')

    class Meta:
        fields = ('title', 'dimension')
        model = Ingredient
