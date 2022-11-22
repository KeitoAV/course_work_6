# TODO здесь производится настройка пермишенов для нашего проекта
from rest_framework import permissions


class IsAdminOrAdOwner(permissions.BasePermission):
    message = 'Объявления могут обновляться только владельцем объявления или администратором.'

    def has_object_permission(self, request, view, obj):
        if request.user.is_user and obj.author != request.user:
            return False
        return True
