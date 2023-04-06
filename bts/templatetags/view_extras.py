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
