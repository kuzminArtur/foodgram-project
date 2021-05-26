from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import UniqueConstraint
from slugify import slugify

User = get_user_model()


class Ingredient(models.Model):
    """Ingredient model."""
    title = models.CharField(max_length=256, verbose_name='Название')
    unit = models.CharField(max_length=128, verbose_name='Еденицы измерения')

    class Meta:
        ordering = ['title']
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return f'{self.title}, {self.unit}'


class Tag(models.Model):
    """Tag model."""

    class Meal(models.TextChoices):
        """Choices for tag."""
        BREAKFAST = 'Завтрак',
        LUNCH = 'Обед',
        DINNER = 'Ужин'

    title = models.CharField(
        unique=True,
        max_length=20,
        verbose_name='Название',
        choices=Meal.choices
    )

    color = models.CharField(
        max_length=20,
        verbose_name='Цвет'
    )
    slug = models.SlugField(unique=True, verbose_name='Уникальный URL')

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.title


class Recipe(models.Model):
    """Recipe model."""
    title = models.CharField(max_length=256, verbose_name='Название')
    author = models.ForeignKey(
        User, related_name='recipes',
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )
    text = models.TextField(verbose_name='Описание')
    time_cooking = models.PositiveIntegerField(
        verbose_name='Время приготовленния',
        validators=[
            MinValueValidator(1),
        ],
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

    class Meta:
        ordering = ['-pub_date', ]
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def save(self, **kwargs):
        """Append slug field value."""
        if not self.slug and self.id:
            self.slug = slugify(f'{self.title}-{self.id}')
        super().save(**kwargs)

    def __str__(self):
        return self.title


class RecipeIngredient(models.Model):
    """Many-to-many relationship for Recipe and Ingredient model."""
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
    amount = models.PositiveIntegerField(
        verbose_name='Количество',
        validators=[
            MinValueValidator(1),
        ],
    )

    class Meta:
        verbose_name = 'Связь рецепт-ингредиент'
        verbose_name_plural = 'Связи рецепт-ингредиент'

    def __str__(self):
        return f'{self.ingredient.title} - {self.amount} {self.ingredient}'


class Favorite(models.Model):
    """Model for favorite relation between User and Recipe models."""
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

    class Meta:
        verbose_name = 'Избранное. Связь пользователь-рецепт'
        verbose_name_plural = 'Избранное. Связи пользователь-рецепт'
        constraints = [
            UniqueConstraint(fields=['user', 'recipe'], name='unique_favorite')
        ]


class Follow(models.Model):
    """Model for follow relation between two User."""
    user = models.ForeignKey(
        User,
        related_name='follower',
        on_delete=models.CASCADE,
        verbose_name='Подписчик',
    )
    author = models.ForeignKey(
        User,
        related_name='following',
        on_delete=models.CASCADE,
        verbose_name='Автор',
    )

    class Meta:
        verbose_name = 'Подписка. Связь пользователь-пользователь'
        verbose_name_plural = 'Подписки. Связи пользователь-пользователь'
        constraints = [
            UniqueConstraint(fields=['user', 'author'], name='unique_follow')]

    def clean(self):
        if self.author == self.user:
            raise ValueError('Подписка на самого себя не разрешена')


class Purchase(models.Model):
    """Model for purchase relation between User and Recipe models."""
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='purchases',
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, verbose_name='Рецепт в покупках',
    )

    class Meta:
        verbose_name = 'Покупка. Связь пользователь-рецепт'
        verbose_name_plural = 'Покупки. Связи пользователь-рецепт'
        constraints = [
            UniqueConstraint(fields=['user', 'recipe'], name='unique_purchase')
        ]
