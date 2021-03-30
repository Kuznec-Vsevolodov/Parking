from django.urls import path, include
from .views import PlaceListView, PlaceDetailView, SectorDetailView, SectorListView, Parking_placeDetailView, BookingListView, ParkingPlaceListView, WalletListView, WalletDetailView, RegisterView

urlpatterns = [
    path('places/', PlaceListView.as_view()),
    path('places/<int:pk>/', PlaceDetailView.as_view()),
    path('sectors/', SectorListView.as_view()),
    path('sectors/<int:pk>/', SectorDetailView.as_view()),
    path('parking_places/', ParkingPlaceListView.as_view()),
    path('parking_places/<int:pk>/', Parking_placeDetailView.as_view()),
    path('booked_places/', BookingListView.as_view()),
    path('wallets/', WalletListView.as_view()),
    path('wallets/<int:pk>/', WalletDetailView.as_view()),
    path('register/', RegisterView.as_view()),
]