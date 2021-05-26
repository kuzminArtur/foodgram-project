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
    if remainder == 1:
        return f'{num} {ending[0]}'
    if 1 < remainder <= 4:
        return f'{num} {ending[1]}'
    return f'{num} {ending[2]}'
