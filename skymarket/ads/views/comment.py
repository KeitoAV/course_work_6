from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from drf_spectacular.utils import extend_schema_view, extend_schema
from ads.models.ad import Ad
from ads.models.comment import Comment
from ads.permissions import IsAdminOrAdOwner
from ads.serializers.comment import CommentSerializer, CommentCreateSerializer


@extend_schema_view(
    list=extend_schema(summary="Получает список всех комментариев к объявлению, указанному в 'ad_id'"),
    create=extend_schema(summary="Создает новый комментарий к указанному объявлению"),
    retrieve=extend_schema(summary="Извлекает комментарий по 'pk'"),
    destroy=extend_schema(summary="Удаляет комментарий по 'pk'"),
    partial_update=extend_schema(summary="Обновляет комментарий по 'pk'"),
)
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'patch', 'delete', 'post']

    def get_queryset(self):
        """
        Возвращает список всех комментариев для
        объявления, как определено частью ad_pk URL-адреса.
        """
        ad_id = self.kwargs['ad_pk']
        return self.queryset.filter(ad__id=ad_id)

    def get_permissions(self):
        """Создает экземпляр и возвращает список разрешений, которые требуются этому представлению."""

        if self.action in ('retrieve', 'create'):
            permission_classes = [IsAuthenticated]
        elif self.action in ('update', 'destroy', 'partial_update'):
            permission_classes = [IsAuthenticated, IsAdminOrAdOwner]
        else:
            permission_classes = [IsAuthenticatedOrReadOnly]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        """Возвращает класс сериализатора для каждого метода."""

        if self.action == 'retrieve':
            return CommentSerializer
        elif self.action in ("create", "partial_update", "update"):
            return CommentCreateSerializer
        else:
            return CommentSerializer

    def perform_create(self, serializer):
        """Создает комментарий к объявлению, указанному в ad_pk. """
        ad_id = self.kwargs['ad_pk']
        ad = get_object_or_404(Ad, id=ad_id)
        serializer.save(author=self.request.user, ad=ad)

    def perform_update(self, serializer):
        """Обновляет комментарий к объявлению, указанному в параметре ad_pk. """
        user = self.request.user
        if user.is_user or user.is_admin:
            ad_id = self.kwargs['ad_pk']
            ad = get_object_or_404(Ad, id=ad_id)
            serializer.save(author=self.request.user, ad=ad)
