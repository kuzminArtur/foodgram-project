# Generated by Django 3.2.1 on 2021-05-26 15:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0012_auto_20210523_1435'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='favorite',
            options={'verbose_name': 'Избранное. Связь пользователь-рецепт', 'verbose_name_plural': 'Избранное. Связи пользователь-рецепт'},
        ),
        migrations.AlterModelOptions(
            name='follow',
            options={'verbose_name': 'Подписка. Связь пользователь-пользователь', 'verbose_name_plural': 'Подписки. Связи пользователь-пользователь'},
        ),
        migrations.AlterModelOptions(
            name='ingredient',
            options={'ordering': ['title'], 'verbose_name': 'Ингредиент', 'verbose_name_plural': 'Ингредиенты'},
        ),
        migrations.AlterModelOptions(
            name='purchase',
            options={'verbose_name': 'Покупка. Связь пользователь-рецепт', 'verbose_name_plural': 'Покупки. Связи пользователь-рецепт'},
        ),
        migrations.AlterModelOptions(
            name='recipe',
            options={'ordering': ['-pub_date'], 'verbose_name': 'Рецепт', 'verbose_name_plural': 'Рецепты'},
        ),
        migrations.AlterModelOptions(
            name='recipeingredient',
            options={'verbose_name': 'Связь рецепт-ингредиент', 'verbose_name_plural': 'Связи рецепт-ингредиент'},
        ),
        migrations.AlterModelOptions(
            name='tag',
            options={'verbose_name': 'Тег', 'verbose_name_plural': 'Теги'},
        ),
        migrations.AlterField(
            model_name='tag',
            name='slug',
            field=models.SlugField(unique=True, verbose_name='Уникальный URL'),
        ),
        migrations.AddConstraint(
            model_name='favorite',
            constraint=models.UniqueConstraint(fields=('user', 'recipe'), name='unique_favorite'),
        ),
    ]
