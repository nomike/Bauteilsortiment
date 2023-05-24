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

from rest_framework import serializers

from bts.models import *


class LabelTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = LabelType
        fields = [
            "id",
            "name",
            "width",
            "height",
            "lines_per_row",
            "rows_per_label",
        ]


class LocationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Location
        fields = [
            "id",
            "name",
        ]


class AssortmentBoxSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = AssortmentBox
        fields = [
            "id",
            "name",
            "location",
            "coordinates",
            "color",
            "layout",
        ]


class MerchantSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Merchant
        fields = [
            "id",
            "name",
            "url",
            "description",
        ]
