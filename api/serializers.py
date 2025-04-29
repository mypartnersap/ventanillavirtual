from django.contrib.auth.models import User, Group
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class FileUploadSerializer(serializers.Serializer):
    # I set use_url to False so I don't need to pass file 
    # through the url itself - defaults to True if you need it
    file = serializers.FileField(use_url=False)