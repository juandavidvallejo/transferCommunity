from rest_framework import permissions


class IsSenderOfMoney(permissions.BasePermission):
    def has_object_permission(self, request, view, giros):
        if request.user:
            return giros.sender == request.user
        return False