from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User, Group


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'id', 'name')


class UserSerializer(serializers.ModelSerializer):
    groups = GroupSerializer(many=True, read_only=True)
    groups_ids = serializers.PrimaryKeyRelatedField(queryset=Group.objects.all(), many=True, write_only=True,
                                                    required=False)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('url', 'id', 'username', 'email',
                  'password', 'is_superuser', 'groups', 'groups_ids')

    def create(self, validated_data):
        groups = validated_data.pop('groups_ids', None)
        instance = User(**validated_data)
        instance.save()
        if groups:
            for group in groups:
                instance.groups.add(group)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        groups = validated_data.pop('groups_ids', None)
        if groups is not None:
            instance.groups.clear()
            for group in groups:
                instance.groups.add(group)
        instance.save()
        return instance


class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = '__all__'


class PlacaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Placa
        fields = '__all__'


class RecorteRetangularSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecorteRetangular
        fields = '__all__'


class RecorteTriangularSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecorteTriangular
        fields = '__all__'


class RecorteCircularSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecorteCircular
        fields = '__all__'
