from django import template

register = template.Library()


@register.filter
def addclass(field, css):
    return field.as_widget(attrs={"class": css})


@register.filter
def get_num_ending(num, ending):
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
