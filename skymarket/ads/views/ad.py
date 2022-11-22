from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema_view, extend_schema
from ads.filters import AdFilter
from ads.models.ad import Ad
from ads.permissions import IsAdminOrAdOwner
from ads.serializers.ad import AdListSerializer, AdDetailSerializer, AdCreateSerializer


@extend_schema_view(
    list=extend_schema(summary="Получает список всех объявлений"),
    create=extend_schema(summary="Создает новое объявление"),
    retrieve=extend_schema(summary="Получает объявление по 'pk'"),
    destroy=extend_schema(summary="Удаляет объявление по 'pk'"),
    partial_update=extend_schema(summary="Обновляет объявление по 'pk'"),
    list_user_ads=extend_schema(summary="Получает список объявлений пользователя"),
)
class AdViewSet(viewsets.ModelViewSet):
    queryset = Ad.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = AdFilter
    serializer_class = AdListSerializer
    http_method_names = ['get', 'patch', 'delete', 'post']

    def get_serializer_class(self):
        """Возвращает класс сериализатора для каждого метода."""
        if self.action == 'retrieve':
            return AdDetailSerializer
        elif self.action in ("create", "partial_update", "update"):
            return AdCreateSerializer
        else:
            return AdListSerializer

    def get_permissions(self):
        """Создает экземпляр и возвращает список разрешений, которые требуются этому представлению."""
        if self.action in ('retrieve', 'create'):
            permission_classes = [IsAuthenticated]
        elif self.action in ('update', 'destroy', 'partial_update'):
            permission_classes = [IsAuthenticated, IsAdminOrAdOwner]
        else:
            permission_classes = [IsAuthenticatedOrReadOnly]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        user = self.request.user
        if user.is_user or user.is_admin:
            serializer.save(author=self.request.user)

    @action(methods=['get'], detail=False, permission_classes=[IsAuthenticated, IsAdminOrAdOwner],
            url_path='me', url_name='list_user_ads')
    def list_user_ads(self, request, pk=None):
        """Возвращает список всех объявлений, размещенных пользователем."""
        user = self.request.user
        self.queryset = user.ads
        return self.list(request, pk=None)
