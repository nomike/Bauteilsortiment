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

import re

from django import template
from django.db import models

from django.template.loader_tags import do_include

register = template.Library()


@register.tag("include_maybe")
def do_include_maybe(parser, token):
    "Source: http://stackoverflow.com/a/18951166/15690"
    bits = token.split_contents()
    if len(bits) < 2:
        raise template.TemplateSyntaxError(
            "%r tag takes at least one argument: "
            "the name of the template to be included." % bits[0]
        )

    try:
        silent_node = do_include(parser, token)
    except template.TemplateDoesNotExist:
        # Django < 1.7
        return ""

    _orig_render = silent_node.render

    def wrapped_render(*args, **kwargs):
        try:
            return _orig_render(*args, **kwargs)
        except template.TemplateDoesNotExist:
            return ""

    silent_node.render = wrapped_render
    return silent_node


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
        value = template.Variable(f"object.{attr}").resolve(pseudo_context)
    except template.VariableDoesNotExist:
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
    """

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
def get_type_plural(object):
    """
    Returns the type of an object as a string.
    """

    return object._meta.verbose_name_plural


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
