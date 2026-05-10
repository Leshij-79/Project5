from rest_framework import permissions


class IsModerator(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name="Moderator").exists()


class IsNotModerator(permissions.BasePermission):
    def has_permission(self, request, view):
        return not request.user.groups.filter(name="Moderator").exists()


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class IsOwnerOrNotModerator(permissions.BasePermission):
    def has_permission(self, request, view):
        # Проверяем, есть ли объект (для destroy)
        if view.action == 'destroy':
            obj = view.get_object()
            # Разрешаем удаление если:
            # 1. Пользователь - владелец
            # 2. И пользователь НЕ модератор
            return (obj.owner == request.user and
                   not request.user.groups.filter(name="Moderator").exists())
        return True
