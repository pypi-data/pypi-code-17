from rest_framework import serializers

from django.contrib.auth.models import User, Group
from .models import Asset, Property, EnumerationChoice, ChoiceProperty, EnumerationType

import assetadapter


class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Group
        fields = ('url', 'name')


class PropertyUnitChoiceListSerializer(serializers.ModelSerializer):

    class Meta:
        model = EnumerationChoice
        fields = ('id', 'value')


class EnumerationTypeSerializer(serializers.ModelSerializer):
    choice_set = PropertyUnitChoiceListSerializer(read_only=True, many=True)

    class Meta:
        model = EnumerationType
        fields = ('id', 'display_name', 'description', 'choice_set')


class PropertySerializer(serializers.ModelSerializer):
    unit_choices = EnumerationTypeSerializer(read_only=True)

    class Meta:
        model = Property
        fields = (
        'id', 'name', 'display_name', 'description', 'type', 'getter_command', 'setter_command', 'unit_choices',
        'default_unit')


class AssetListSerializer(serializers.ListSerializer):
    properties = PropertySerializer(many=True, read_only=True)

    class Meta:
        model = Asset
        fields = ('alias', 'address', 'id', 'properties', 'display_name', 'description')


class AssetSerializer(serializers.ModelSerializer):
    properties = PropertySerializer(many=True, read_only=True)

    class Meta:
        model = Asset
        fields = ('alias', 'address', 'id', 'properties', 'display_name', 'description')
