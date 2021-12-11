from typing_extensions import Required
from rest_framework import serializers
from core.models import User, Bookmark
from rest_framework.validators import UniqueTogetherValidator

class BookmarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookmark
        fields = ['title', 'url', 'user', 'public']
        extra_kwargs = {'public': {'required': False}}
        validators = [
            UniqueTogetherValidator(
                queryset=Bookmark.objects.all(),
                fields=['user', 'url']
            )
        ]

class BookmarkQueryParamsSerializer(serializers.Serializer):
    user_id = serializers.IntegerField(required=False)

