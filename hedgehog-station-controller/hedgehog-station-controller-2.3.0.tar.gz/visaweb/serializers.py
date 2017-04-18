from rest_framework import serializers

from django.contrib.auth.models import User, Group
from .models import Asset, Property

import assetadapter
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')

class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = ('name', 'display_name', 'description', 'type')


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