from django import forms

from .models import Recipe


class RecipeForm(forms.ModelForm):
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

