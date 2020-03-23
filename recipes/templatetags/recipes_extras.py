from django import template
from ..models import Recipe

register = template.Library()



@register.simple_tag
def total_recipes():
	return Recipe.objects.count()



@register.filter
def endline_split(value):
    return value.split('\n')
