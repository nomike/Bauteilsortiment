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

import inspect

from rest_framework import serializers

import bts.models
from bts.models import *


class GenericSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = None
        fields = None


for name in [
    obj.__name__
    for name, obj in bts.models.__dict__.items()
    if inspect.isclass(obj) and issubclass(obj, models.Model)
]:
    generated_class = type(
        name + "Serializer",
        (GenericSerializer,),
        {
            "model": getattr(bts.models, name),
            "fields": [field.name for field in getattr(bts.models, name)._meta.fields],
        },
    )
    globals()[generated_class.__name__] = generated_class
