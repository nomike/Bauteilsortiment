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
def get_id(field: models.ForeignKey):
    if not isinstance(field, models.ForeignKey):
        return ""
    return field


@register.simple_tag
def cat(str1, str2):
    return str1 + str2


@register.simple_tag
def get_detail_name(field: models.ForeignKey, suffix):
    return str(re.sub(r'(?<!^)(?=[A-Z])', '_', field.related_model.__name__).lower()) + suffix


@register.filter
def snake_case(string):
    return str(re.sub(r'(?<!^)(?=[A-Z])', '_', string).lower())


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
def get_model_fields(model: models.Model):
    return model._meta.fields


@register.filter
def get_list_fields(model: models.Model):
    return model.meta_list_fields


@register.filter
def get_meta_list_detail_link_fields(model: models.Model):
    return model.meta_list_detail_link_fields


@register.simple_tag
def get_verbose_name(model: models.Model):
    return model._meta.verbose_name.capitalize()


@register.filter
# Gets the name of the passed in field on the passed in object
def verbose_field_name(object, field):
    # Check if the verbose name is using the default value, in which case it will be all lowercase
    if object._meta.get_field(field).verbose_name.islower:
        # Change
        return object._meta.get_field(field).verbose_name.capitalize()
    else:
        # The verbose name has been set in the model, so just display it normally
        return object._meta.get_field(field).verbose_name
