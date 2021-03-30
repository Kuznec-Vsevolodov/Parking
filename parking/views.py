from .models import Place, Event, Sector, ParkingPlace, Booking, Wallet
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from rest_framework import viewsets, permissions
from .serializers import PlaceSerializer, Parking_placeSerializer, SectorSerializer, EventSerializer, BookingSerializer, WalletSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.permissions import IsAdminUser, IsAuthenticatedOrReadOnly, AllowAny, IsAuthenticated
from .custom_permissions import IsOwner, isPlaceOwner
from .services import ParkingPlacesServices
# Create your views here.


class PlaceDetailView(APIView):

    permission_classes = [isPlaceOwner]

    def get(self, request, pk):
        post = Place.objects.get(id=pk)
        serializer = PlaceSerializer(post, many=False)
        return Response(serializer.data)

    def delete(self, request, pk, format=None):
        snippet = Place.objects.get(id=pk)
        snippet.delete()
        return Response()

    def put(self, request, pk, *args, **kwargs):
        current_data = Place.objects.get(id=pk)
        current_data.__dict__
        update_serializer = PlaceSerializer(current_data, data={'title': request.data['title'], 'address': request.data['address'], 'general_scheme': request.data['general_scheme'] })
        if update_serializer.is_valid():
            update_serializer.save()
        return Response(update_serializer.data)

    # def post(self, request, pk, *args, **kwargs):
    #
    #     return Response(serializer.data)

class PlaceListView(APIView):


    def get(self, request):
        posts = Place.objects.all()
        serializer = PlaceSerializer(posts, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = PlaceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data)

    permission_classes = [IsOwner]
class SectorDetailView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    def get(self, request, pk):
        sector = Sector.objects.get(id=pk)
        serializer = SectorSerializer(sector, many=False)
        return Response(serializer.data)

    def delete(self, request, pk, format=None):
        snippet = Sector.objects.get(id=pk)
        snippet.delete()
        return Response()

    def put(self, request, pk, format=None):
        snippet = Sector.objects.get(id=pk)
        serializer = SectorSerializer(snippet, data=request.data)
        snippet = snippet.__dict__
        if serializer.is_valid():
            if snippet['rows'] > request.data['rows'] or snippet['columns'] > request.data['columns']:
                ParkingPlacesServices.deleter(self, request, snippet)
            elif snippet['rows'] < request.data['rows'] or snippet['columns'] < request.data['columns']:
                ParkingPlacesServices.add_new_places(self, request, snippet)
            serializer.save()
            return Response(serializer.data)
        return Response()


class SectorListView(APIView):

    def get(self, request):
        sectors = Sector.objects.all()
        serializer = SectorSerializer(sectors, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):

        serializer = SectorSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            current_sector = Sector.objects.order_by('-id')[0]
            current_sector = current_sector.__dict__
            ParkingPlacesServices.create(self, current_sector, request)
        return Response(serializer.data)

class PlaceViewSet(viewsets.ModelViewSet):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer
    permission_classes = [IsAuthenticated]

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

class SectorViewSet(viewsets.ModelViewSet):
    queryset = Sector.objects.all()
    serializer_class = SectorSerializer

class Parking_placeViewSet(viewsets.ModelViewSet):
    queryset = ParkingPlace.objects.all()
    serializer_class = Parking_placeSerializer

class ParkingPlaceListView(APIView):
    def get(self, request):
        places = ParkingPlace.objects.all()
        serializer = Parking_placeSerializer(places, many=True)
        return Response(serializer.data)

class Parking_placeDetailView(APIView):
    def get(self, request, pk):
        place = ParkingPlace.objects.get(id=pk)
        serializer = Parking_placeSerializer(place, many=False)
        return Response(serializer.data)

    def post(self, request, pk, *args, **kwargs):
        serializer = Parking_placeSerializer(data={'user_id': 1, 'parking_place_id': pk})
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)

class BookingListView(APIView):
    def get(self, request):
        booked_places = Booking.objects.all()
        serializer = BookingSerializer(booked_places, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        current_user = request.user
        wallet = Wallet.objects.get(user=current_user.id)
        place = ParkingPlace.objects.get(id=request.data['parking_place'])
        place.__dict__
        sector = Sector.objects.get(id=place.sector_id.pk)
        if Booking.objects.filter(parking_place = place.pk).exists() != True:
            if wallet.wallet >= sector.price:
                serializer = BookingSerializer(data={'user': current_user.id, 'parking_place': request.data['parking_place'], 'event': request.data['event_id']})
                if serializer.is_valid():
                    serializer.save()
                    wallet_serializer = WalletSerializer(wallet, data={'user': current_user.id, 'wallet': wallet.wallet - sector.price})
                    if wallet_serializer.is_valid():
                        wallet_serializer.save()
                return Response(serializer.data)
        else:
            return Response("This place is already booked")

class WalletListView(APIView):
    def get(self, request):
        wallets = Wallet.objects.all()
        serializer = WalletSerializer(wallets, many=True)
        return Response(serializer.data)

    def post(self, request):
        user = request.user
        serializer = WalletSerializer(data={'user': user.id, 'wallet': request.data['wallet']})
        serializer.is_valid()
        serializer.save()
        return Response(serializer.data)

class WalletDetailView(APIView):
    def get(self, request, pk):
        wallet = Wallet.objects.get(id=pk)
        serializer = WalletSerializer(wallet, many=False)
        return Response(serializer.data)

    def delete(self, request, pk, format=None):
        snippet = Wallet.objects.get(id=pk)
        snippet.delete()
        return Response()

    def put(self, request, pk, *args, **kwargs):
        current_data = Wallet.objects.get(id=pk)
        current_data.__dict__
        update_serializer = WalletSerializer(current_data, data={'user': request.user.id, 'wallet': current_data.wallet+request.data['income']})
        if update_serializer.is_valid():
            update_serializer.save()
        return Response(update_serializer.data)


class RegisterView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        user = User.objects.create_user(request.data['username'], request.data['email'], request.data['password'])
        token = Token.objects.create(user=user)
        print(user.is_owner)
        user.save()
        serializer = WalletSerializer(data={'user': user.id, 'wallet': 0})
        serializer.is_valid()
        serializer.save()
        return Response("User " + user.username + "is registered")