from rest_framework import permissions
from .models import UserType, Place, User, Wallet, Event

class walletOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        wallet = Wallet.objects.get(id=view.kwargs['pk'])
        wallet.__dict__
        if wallet.user == request.user:
            return True

        return False

class eventOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        event = Event.objects.get(id=view.kwargs['pk'])
        event.__dict__
        place = Place.objects.get(id=event.place.pk)
        if place.owner == request.user:
            return True

        return False

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