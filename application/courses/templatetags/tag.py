from django import template
from ..models import Material,Answer

register = template.Library()

@register.simple_tag
def getMaterials(notice):
    
    materials = Material.objects.filter(notice=notice)
    
    return materials

@register.simple_tag
def getAnswers(question):

    answers = Answer.objects.filter(question=question)
    
    return answers