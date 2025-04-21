from django import template

register = template.Library()

@register.filter
def dict_lookup(lst, key):
  return next((item['chat_history'] for item in lst if item['chat_list']['id'] == key), [])