from django.core.management.base import BaseCommand

from recipes.models import Tag

TAG_COLOR = {
    'Завтрак': ('orange', 'breakfast'),
    'Обед': ('green', 'lunch'),
    'Ужин': ('purple', 'dinner'),
}


class Command(BaseCommand):
    help = 'Create tags'

    def handle(self, *args, **options):
        for title, fields in TAG_COLOR.items():
            color, slug = fields
            tag = Tag.objects.get_or_create(title=title, color=color,
                                            slug=slug)
