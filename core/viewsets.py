from rest_framework import  viewsets
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from core.serializers import BookmarkSerializer, BookmarkQueryParamsSerializer
from rest_framework.authentication import  TokenAuthentication
from core.models import Bookmark
from rest_framework.response import Response
from rest_framework import status


class BookmarkViewSet(viewsets.ModelViewSet):
    queryset = Bookmark.objects.all()
    serializer_class = BookmarkSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        return [] if self.action in ['list', 'retrieve'] else [IsAuthenticated()]


    def partial_update(self, request, pk=None, partial=True, **kwargs):

        if not pk:
            raise NotFound


        user = request.user

        bk = Bookmark.objects.filter(pk=pk, user=user)

        if not bk.exists():
            raise NotFound


        if partial:
            qp = BookmarkSerializer(bk.first(), data=request.data, partial=True)
        else:
            qp = BookmarkSerializer(bk.first(), data=request.data)
        qp.is_valid(raise_exception=True)
        qp.save()

        return Response(qp.data, status=status.HTTP_200_OK)

    def update(self, request, pk=None, **kwargs):
        return self.partial_update(request, pk, partial=False)



    def destroy(self, request, pk=None):

        if not pk:
            raise NotFound

        user = request.user

        bk = Bookmark.objects.filter(pk=pk, user=user)

        if not bk.exists():
            raise NotFound

        bk.delete()
        return Response(status=status.HTTP_200_OK)


    def list(self, request, pk=None):
        qp = BookmarkQueryParamsSerializer(data=request.query_params)
        qp.is_valid(raise_exception=True)
        user_id = qp.data.pop('user_id', None)



        user = request.user
        if user.is_authenticated:
            if not user_id:
                return Response(Bookmark.objects.filter(user=user).values(), status=status.HTTP_200_OK)
            if user_id == user.id:
                return Response(Bookmark.objects.filter(user=user_id).values(), status=status.HTTP_200_OK)
            return Response(Bookmark.objects.filter(user=user_id, public=True).values(), status=status.HTTP_200_OK)

        if not pk and not user_id:
            return Response(Bookmark.objects.filter(public=True).values(), status=status.HTTP_200_OK)

        if not pk:
            return Response(Bookmark.objects.filter(user=user_id, public=True).values(), status=status.HTTP_200_OK)

        return Response(Bookmark.objects.filter(pk=pk, public=True).values(), status=status.HTTP_200_OK)


