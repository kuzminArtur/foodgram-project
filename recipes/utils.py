import io

from django.conf import settings
from django.shortcuts import get_object_or_404
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

from recipes.models import RecipeIngredient, Ingredient


def add_ingredients(post_data, recipe):
    """Create ingredients for recipe."""
    RecipeIngredient.objects.filter(recipe=recipe).delete()
    recipe_ingredients = []
    for key, value in post_data.items():
        if key.startswith('nameIngredient'):
            num = key.split('_')[1]
            ingredient = get_object_or_404(Ingredient, title=value)
            recipe_ingredients.append(
                RecipeIngredient(
                    recipe=recipe,
                    ingredient=ingredient,
                    amount=post_data[f'valueIngredient_{num}']
                )
            )
    RecipeIngredient.objects.bulk_create(recipe_ingredients)


def get_pdf(data):
    """Return buffer with pdf-data."""
    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer)
    pdfmetrics.registerFont(TTFont('DejaVuSans',
                                   settings.BASE_DIR /
                                   'recipes/fonts/DejaVuSans.ttf'))
    pdf.setFont("DejaVuSans", 14)
    text_object = pdf.beginText(mm * 10, mm * 280)

    text_object.textLine('Для приготовления блюд вам потребуется:')
    pdf.line(mm * 10, mm * 278, mm * 160, mm * 278)
    text_object.textLine('')

    for i, ingredient in enumerate(data):
        text_object.textLine(f'{ingredient["title"]} - {ingredient["amount"]} '
                             f'{ingredient["unit"]}')
    pdf.drawText(text_object)
    pdf.showPage()
    pdf.save()
    buffer.seek(0)
    return buffer
