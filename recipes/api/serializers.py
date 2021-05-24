from rest_framework import serializers

from ..models import Ingredient, Purchase


class IngredientSerializer(serializers.ModelSerializer):
    """Rename field unit to dimension."""
    dimension = serializers.CharField(source='unit')

    class Meta:
        fields = ('title', 'dimension')
        model = Ingredient


class PurchaseSerialiser:
    class Meta:
        fields = ('recipe',)
        model = Purchase
