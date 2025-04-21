from django import template

register = template.Library()

@register.filter
def mul(value, arg):
    """Multiplies the value by the argument."""
    try:
        return int(value) * int(arg)
    except (ValueError, TypeError):
        return value

def sort_by_timestamp(comments):
    return sorted(comments, key=lambda comment: comment.timestamp, reverse=True)

register.filter('sort_comments',sort_by_timestamp)
