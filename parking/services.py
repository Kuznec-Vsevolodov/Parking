from .serializers import Parking_placeSerializer
from .models import Sector, ParkingPlace

class IncludeMethods():
    def columns_create(self, request, sector, i, j):
        while j <= request.data["columns"]:
            new_serializer = Parking_placeSerializer(
                data={'row': i, 'column': j, 'sector_id': sector['id']})
            if new_serializer.is_valid():
                new_serializer.save()
            j += 1

class ParkingPlacesServices():
    def create(self, current_sec, request):
        i = 1
        j = 1
        while i <= request.data["rows"]:
            IncludeMethods.columns_create(self, request, current_sec, i, j)
            j = 1
            i += 1

    def delete(self, request, snippet):
        places = ParkingPlace.objects.filter(sector_id=snippet['id']).order_by('row')
        print(places)
        for place in places:
            place = place.__dict__
            current_place = ParkingPlace.objects.get(id=place['id'])
            if place['row'] > request.data['rows'] or place['column'] > request.data['columns']:
                current_place.delete()

    def add_new_places(self, request, sector):
        i = 1
        j = sector['columns'] + 1
        while i <= request.data["rows"]:
            if i > sector['rows']:
                j = 1
            IncludeMethods.columns_create(self, request, sector, i, j)
            j = sector['columns'] + 1
            i += 1