from django import template

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
    new_get_params = request.GET.copy()
    current_tags = request.GET.getlist('filter_tag')
    if tag.slug in current_tags:
        current_tags.remove(tag.slug)
    else:
        current_tags.append(tag.slug)
    new_get_params.setlist('filter_tag', current_tags)
    return new_get_params.urlencode()


@register.simple_tag
def activate_tag(request, tag):
    current_tags = request.GET.getlist('filter_tag')
    if tag.slug in current_tags:
        return 'tags__checkbox_active'
