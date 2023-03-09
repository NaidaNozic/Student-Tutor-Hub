from django import template
from ..models import Material

register = template.Library()

@register.simple_tag
def getMaterials(notice):
    
    materials=Material.objects.filter(notice=notice)
    
    return materials