from rest_framework import permissions


class IsMessageOwner(permissions.BasePermission):  # creating costum permission

    message = 'Permission denied. You can access only to the messages that you own.'

    def has_object_permission(self, request, view, singleMessage):
        return singleMessage.sender == request.user or singleMessage.receiver == request.user
