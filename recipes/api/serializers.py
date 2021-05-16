from rest_framework import serializers

from ..models import Ingredient


class IngredientSerializer(serializers.ModelSerializer):
    dimension = serializers.CharField(source='unit')
    class Meta:
        fields = ('title', 'dimension')
        model = Ingredient
