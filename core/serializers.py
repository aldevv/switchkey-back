from rest_framework import serializers
from core.models import BuyHistory, Product, User
from django.conf import settings
from os.path import exists


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name", "email", "history"]


class RegisterUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "password", "first_name", "last_name", "email"]

    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data["password"])
        return user


class BuyBodySerializer(serializers.Serializer):
    product = serializers.IntegerField()

    def validate_product(self, data):
        try:
            product = Product.objects.get(pk=data)
        except Product.DoesNotExist:
            product = None

        if product:
            return data

        raise serializers.ValidationError("Product Not Found")


class BuyHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BuyHistory
        fields = ["user", "product", "count"]


class ProductSerializer(serializers.ModelSerializer):
    image = serializers.CharField()

    class Meta:
        model = Product
        fields = ["id", "name", "price", "image", "stock"]
