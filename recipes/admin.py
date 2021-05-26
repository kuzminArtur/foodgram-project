from django.contrib import admin

from recipes.models import (Ingredient, Recipe, RecipeIngredient, Tag,
                            Favorite, Follow)


class RecipeIngredientInLine(admin.StackedInline):
    model = RecipeIngredient
    extra = 1
    autocomplete_fields = ('ingredient',)
    verbose_name = 'Ингредиент'
    min_num = 1


@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'ingredient')
    search_fields = ('recipe', 'ingredient')


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'author')
    list_filter = ('title', 'author__username', 'tags__title')
    search_fields = ('title', 'author__username')
    inlines = [RecipeIngredientInLine]
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('title', 'unit')
    list_filter = ('title',)
    search_fields = ('title',)


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')


admin.site.register(Tag)
admin.site.register(Follow)
