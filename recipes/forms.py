from django import forms

from .models import Recipe


class RecipeForm(forms.ModelForm):
    """Recipe create/edit form."""
    class Meta:
        model = Recipe
        fields = (
            'title',
            'tags',
            'time_cooking',
            'text',
            'image',
        )
        widgets = {
            'tags': forms.CheckboxSelectMultiple(),
        }
