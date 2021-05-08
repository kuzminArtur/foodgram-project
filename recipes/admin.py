from django.contrib import admin

from recipes.models import Ingredient, Recipe, RecipeIngredient, Tag, Favorite


class RecipeIngredientInLine(admin.StackedInline):
    model = RecipeIngredient
    extra = 1
    autocomplete_fields = ('ingredient',)
    verbose_name = 'Ингредиент'


@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'ingredient')
    search_fields = ('recipe', 'ingredient')


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'user')
    list_filter = ('title', 'user__username', 'tags__title')
    search_fields = ('title', 'user__username')


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('title', 'unit')
    list_filter = ('title',)
    search_fields = ('title',)


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')
    inlines = [FavoriteInLine]


admin.site.register(Tag)
