# Bauteilsortiment - An Electronic Component Archival System
# Copyright (C) 2023  nomike
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from django.template import Variable, VariableDoesNotExist, Library
from django.db import models
import re


register = Library()


@register.filter
def dict(object):
    """
    Returns the dictionary of an object.
    """

    # return "foo"
    return object.__dict__


@register.filter
def hash(object, attr):
    """
    Returns the value of an attribute of an object.
    """

    pseudo_context = {"object": object}
    try:
        value = Variable("object.%s" % attr).resolve(pseudo_context)
    except VariableDoesNotExist:
        value = None
    return value


@register.simple_tag
def cat(str1, str2):
    """
    Concatenates two strings.
    """

    return str1 + str2


@register.simple_tag
def get_detail_name(field: models.ForeignKey, suffix):
    """
    Returns the name of the detail view of a foreign key field.
    """"

    return str(re.sub(r"(?<!^)(?=[A-Z])", "_", field.related_model.__name__).lower()) + suffix


@register.filter
def snake_case(string: str):
    """
    Converts a string from camel case to snake case.
    """

    return str(re.sub(r"(?<!^)(?=[A-Z])", "_", string).lower())


@register.filter
def snake_to_space(string: str):
    """
    Converts a string from snake case to space case.
    """

    return string.replace("_", " ").capitalize()


@register.filter
def get_type(object):
    """
    Returns the type of an object as a string.
    """

    return object.__class__.__name__


@register.filter
def get_meta(model: models.Model):
    """
    Returns the meta class of a model.
    """

    return model._meta


@register.simple_tag
def is_url_field(field: models.Field):
    """
    Returns true if the field is a URL field.
    """

    return isinstance(field, models.URLField)


@register.simple_tag
def is_foreign_key_field(field: models.Field):
    """
    Returns true if the field is a foreign key field.
    """

    return isinstance(field, models.ForeignKey)


@register.simple_tag
def get_verbose_name(model: models.Model):
    """
    Returns the verbose name of a model.
    """
    
    return model._meta.verbose_name.capitalize()
