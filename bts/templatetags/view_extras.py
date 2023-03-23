from django.template import Variable, VariableDoesNotExist, Library
from django.db import models
import re


register = Library()


@register.filter
def hash(object, attr):
    pseudo_context = {'object': object}
    try:
        value = Variable('object.%s' % attr).resolve(pseudo_context)
    except VariableDoesNotExist:
        value = None
    return value


@register.simple_tag
def cat(str1, str2):
    return str1 + str2


@register.simple_tag
def get_detail_name(field: models.ForeignKey, suffix):
    return str(re.sub(r'(?<!^)(?=[A-Z])', '_', field.related_model.__name__).lower()) + suffix


@register.filter
def snake_case(string: str):
    return str(re.sub(r'(?<!^)(?=[A-Z])', '_', string).lower())


@register.filter
def snake_to_space(string: str):
    return string.replace('_', ' ').capitalize()


@register.filter
def get_type(object):
    return object.__class__.__name__


@register.simple_tag
def is_url_field(field: models.Field):
    return isinstance(field, models.URLField)


@register.simple_tag
def is_foreign_key_field(field: models.Field):
    return isinstance(field, models.ForeignKey)


@register.simple_tag
def get_verbose_name(model: models.Model):
    return model._meta.verbose_name.capitalize()
