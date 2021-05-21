from django import template

register = template.Library()


@register.filter
def addclass(field, css):
    return field.as_widget(attrs={"class": css})


endings = ['рецепт', 'рецепта', 'рецептов']


@register.filter
def get_num_ending(num, ending):
    num = num % 100
    if 11 <= num <= 19:
        return ending[2]

    num = num % 10
    if num == 0:
        return ending[2]
    if num == 1:
        return ending[0]
    return ending[1]
