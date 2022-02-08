from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from core.models import BuyHistory, Product, User
from core.serializers import (
    BuyBodySerializer,
    BuyHistorySerializer,
    ProductSerializer,
    UserSerializer,
)
from django.conf import settings


class UserViewSet(
    mixins.DestroyModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        return (
            [IsAuthenticated(), IsAdminUser()]
            if self.action in ["list"]
            else super().get_permissions()
        )

    @action(detail=False, methods=["get"])
    def id(self, request):
        if request.user.is_authenticated:
            return Response({"user_id": request.user.id}, status=status.HTTP_200_OK)
        return Response("Not authenticated", status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"])
    def history(self, request):
        user = request.user
        history = BuyHistory.objects.filter(user=user.pk).all()
        return Response(
            BuyHistorySerializer(history, many=True).data, status=status.HTTP_200_OK
        )

    @action(detail=False, methods=["post"])
    def buy(self, request):
        serializer = BuyBodySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user
        product_id = serializer.data.get("product")

        try:
            history = BuyHistory.objects.get(user=user.pk, product=product_id)
            history.count += 1
            history.save()
        except BuyHistory.DoesNotExist:
            product = Product.objects.get(pk=product_id)
            user.history.add(product)
            user.save()
            history = BuyHistory.objects.get(user=user.pk, product=product_id)

        return Response(BuyHistorySerializer(history).data, status=status.HTTP_200_OK)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminUser, IsAuthenticated]

    def get_permissions(self):
        return [] if self.action in ["list", "retrieve"] else super().get_permissions()
