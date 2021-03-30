from rest_framework import permissions
from .models import UserType, Place, User

class IsOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            user = UserType.objects.get(user=request.user.id)
        except:
            return False

        if user.is_owner == True:
            return True

        return False

class isPlaceOwner(permissions.BasePermission):
    def has_permission(self, request, view):

        place = Place.objects.get(id=view.kwargs['pk'])
        place.__dict__
        if place.owner == request.user:
            return True

        return False