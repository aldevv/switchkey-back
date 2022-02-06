from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers
from django.db.models.fields import CharField


class RegisterSerializer(RegisterSerializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)

    def save(self, request):
        user = super().save(request)
        user.first_name, user.last_name = (
            request.data["first_name"],
            request.data["last_name"],
        )
        user.save()
        return user
