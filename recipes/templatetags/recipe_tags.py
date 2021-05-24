from django import template
from urllib.parse import urlencode

register = template.Library()


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
    """Set css class tags__checkbox_active if tag is selected."""
    current_tags = request.GET.getlist('filter_tag')
    if tag.slug in current_tags:
        return 'tags__checkbox_active'


@register.simple_tag
def filter_tag(request):
    """Add current tags to paginator."""
    current_tags = request.GET.getlist('filter_tag')
    if current_tags:
        return f'&{urlencode({"filter_tag": current_tags}, doseq=True)}'
    return ""


@register.simple_tag(takes_context=True)
def get_purchases_count(context):
    """Show purchases count."""
    user = context.request.user
    if user.is_anonymous:
        return ""
    count = user.purchases.count()
    return count
