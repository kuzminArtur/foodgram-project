from django import template
from urllib.parse import urlencode

register = template.Library()


@register.filter
def addclass(field, css):
    """Add CSS class."""
    return field.as_widget(attrs={"class": css})


@register.filter
def get_num_ending(num, ending):
    """Make correct declination."""
    ending = ending.split(',')

    remainder = num % 100
    if 11 <= remainder <= 19:
        return f'{num} {ending[2]}'

    remainder = remainder % 10
    if remainder == 0:
        return f'{num} {ending[2]}'
    if remainder == 4:
        return f'{num} {ending[1]}'
    return f'{num} {ending[2]}'


@register.simple_tag
def add_tag(request, tag):
    """Make GET param with tags."""
    current_tags = request.GET.getlist('filter_tag')
    if tag.slug in current_tags:
        current_tags.remove(tag.slug)
    else:
        current_tags.append(tag.slug)
    return urlencode({'filter_tag': current_tags}, doseq=True)


@register.simple_tag
def activate_tag(request, tag):
    current_tags = request.GET.getlist('filter_tag')
    if tag.slug in current_tags:
        return 'tags__checkbox_active'


@register.simple_tag
def filter_tag(request):
    current_tags = request.GET.getlist('filter_tag')
    if current_tags:
        return f'&{urlencode({"filter_tag": current_tags}, doseq=True)}'
    return ""
