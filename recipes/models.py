from django.db import models
from django.contrib.auth import get_user_model
from slugify import slugify

User = get_user_model()


class Ingredient(models.Model):
    title = models.CharField(max_length=256, verbose_name='Название')
    unit = models.CharField(max_length=128, verbose_name='Еденицы измерения')

    def __str__(self):
        return f'{self.title}, {self.unit}'

    class Meta:
        ordering = ['title']


class Tag(models.Model):
    class Meal(models.TextChoices):
        BREAKFAST = 'Завтрак',
        LUNCH = 'Обед',
        DINNER = 'Ужин'

    title = models.CharField(
        max_length=20,
        verbose_name='Название',
        choices=Meal.choices
    )

    color = models.CharField(
        max_length=20,
        verbose_name='Цвет'
    )
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.title


class Recipe(models.Model):
    title = models.CharField(max_length=256, verbose_name='Название')
    author = models.ForeignKey(
        User, related_name='recipe',
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )
    text = models.TextField(verbose_name='Описание')
    time_cooking = models.PositiveIntegerField(
        verbose_name='Время приготовленния'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient',
        related_name='recipes',
        verbose_name='Ингредиенты'
    )
    image = models.ImageField(upload_to='recipes/', verbose_name='Изображение')
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации'
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='recipes',
        verbose_name='Теги'
    )
    slug = models.SlugField(unique=True, verbose_name='Уникальный URL')

    def save(self, **kwargs):
        if not self.slug and self.id:
            self.slug = slugify(f'{self.title}-{self.id}')
        super().save(**kwargs)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-pub_date', ]


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
        related_name='recipe_ingredient'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='Ингредиент'
    )
    amount = models.PositiveIntegerField(verbose_name='Количество')

    def __str__(self):
        return f'{self.ingredient.title} - {self.amount} {self.ingredient}'


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        related_name='favorite',
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        related_name='fancier',
        on_delete=models.CASCADE,
        verbose_name='Рецепт'
    )
