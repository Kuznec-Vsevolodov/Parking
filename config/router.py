from parking.views import PlaceViewSet, Parking_placeViewSet, SectorViewSet, EventViewSet
from rest_framework import routers

router = routers.DefaultRouter()


router.register('sectors', SectorViewSet)
router.register('events', EventViewSet)
router.register('parking-places', Parking_placeViewSet)