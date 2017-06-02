from rest_framework import permissions


METHODS = dict(
    UD={'PUT', 'DELETE'},
    CR={'POST', 'GET'},
    R={'GET'},
    C={'POST'}
)


class RoomPermissions(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in METHODS['C']:
            return True
        if request.method in METHODS['R']:
            return request.user in obj.members.all()
        if request.method in METHODS['UD']:
            return request.user == obj.owner
        else:
            return False


class MessagePermissions(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in METHODS['CR']:
            return request.user in obj.room.members.all()
        if request.method in METHODS['UD']:
            return request.user == obj.owner
        else:
            return False
