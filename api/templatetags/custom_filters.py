from django import template

register = template.Library()

def sort_by_timestamp(comments):
    return sorted(comments, key=lambda comment: comment.timestamp, reverse=True)

register.filter('sort_comments',sort_by_timestamp)
