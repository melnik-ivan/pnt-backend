from rest_framework import permissions


METHODS = dict(
    UD={'PUT', 'DELETE'},
    CR={'POST', 'GET'},
    R={'GET'},
    C={'POST'}
)


# class IsOwnerOrReadOnly(permissions.BasePermission):
#     """
#     Custom permission to only allow owners of an object to edit it.
#     """
#
#     def has_object_permission(self, request, view, obj):
#         # Read permissions are allowed to any request,
#         # so we'll always allow GET, HEAD or OPTIONS requests.
#         if request.method in permissions.SAFE_METHODS:
#             return True
#
#         # Write permissions are only allowed to the owner.
#         return obj.owner == request.user
#
#
# class IsOwner(permissions.BasePermission):
#     def has_object_permission(self, request, view, obj):
#         return request.user == obj.owner and request.method in METHODS['RUD']
#
#
# class IsInMessageRoomMembers(permissions.BasePermission):
#     """
#     Custom permission to only allow owners of an object to edit it and see it.
#     """
#     def has_object_permission(self, request, view, obj):
#         return request.user in obj.room.members and request.method in METHODS['CR']
#
#
# class IsRoomMember(permissions.BasePermission):
#     """
#     Custom permission to only allow owners of an object to edit it and see it.
#     """
#     def has_object_permission(self, request, view, obj):
#         return (request.user in obj.members.all() and request.method in METHODS['R']) or request.method in METHODS['C']

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
            print(1)
            return request.user in obj.room.members.all()
        if request.method in METHODS['UD']:
            print(2)
            return request.user == obj.owner
        else:
            print(3)
            return False
