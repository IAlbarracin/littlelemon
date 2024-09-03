from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from restaurant import models
from . import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.utils import timezone
from django.contrib.auth.models import User, AnonymousUser
import datetime

def generate_available_times(start=21, end=23, min_interval=5):
    current_datetime = datetime.datetime(year=2024, month=1, day= 1, hour=start)
    end_datetime = datetime.datetime(year=2024, month=1, day=1, hour=end)
    current_time = current_datetime.time()
    available_times = {f'{current_time.strftime('%H:%M')}': 'AVAILABLE'}
    while current_datetime < end_datetime:
        current_datetime += datetime.timedelta(minutes=min_interval)
        current_time = current_datetime.time().strftime('%H:%M')
        available_times.update({current_time: 'AVAILABLE'})
    return available_times

class Users(APIView):
    def post(self, request):
        serializer = serializers.UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.create_user(
            username=serializer.validated_data['username'],
            password=serializer.validated_data['password'],
            email=serializer.validated_data['email']
        )

        return Response(
            serializers.UserSerializer(user).data,
            status=status.HTTP_201_CREATED
        )

class UsersMe(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(
            serializers.UserSerializer(request.user).data,
            status=status.HTTP_200_OK
        )

class MenuAPI(APIView):
    authentication_classes = [TokenAuthentication]

    def get(self, request):
        menu = models.Menu.objects.all()
        serializer = serializers.MenuSerializer(menu, many=True)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )
    
    def post(self, request):
        user = request.user
        if user.groups.filter(name='Manager').exists():
            serializer = serializers.MenuSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            menu_item = models.Menu.objects.create(
                title=serializer.validated_data['title'],
                price=serializer.validated_data['price'],
                inventory=serializer.validated_data['inventory']
            )
            return Response(
                {
                    'detail': 'The item was added to menu successfully',
                    'menu_item': serializers.MenuSerializer(menu_item).data
                },
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                {
                    'detail': 'Only managers are allowed to access this endpoint'
                },
                status=status.HTTP_403_FORBIDDEN
            )
        
class MenuItemAPI(APIView):
    authentication_classes = [TokenAuthentication]

    def get(self, request, id):
        try:
            menu_item = models.Menu.objects.get(id=id)
        except ObjectDoesNotExist:
            return Response(
                {
                    'detail': 'No item in the menu matches the id provided'
                },
                status=status.HTTP_404_NOT_FOUND
            )
        return Response(
            serializers.MenuSerializer(menu_item).data,
            status=status.HTTP_200_OK
        )

    def put(self, request, id):
        user = request.user
        if user.groups.filter(name='Manager').exists():
            try:
                menu_item = models.Menu.objects.get(id=id)
            except ObjectDoesNotExist:
                return Response(
                    {
                        'detail': 'No item in the menu matches the id provided'
                    },
                    status=status.HTTP_404_NOT_FOUND
                )
            serializer = serializers.MenuItemDeserializer(data=request.data)
            if serializer.is_valid():
                validated_data = serializer.validated_data
                if len(validated_data) > 0:
                    for key, value in validated_data.items():
                        setattr(menu_item, key, value)
                    menu_item.save()
                    return Response(
                        {
                            'detail': 'The item in the menu has been updated successfully',
                            'menu_item': serializers.MenuSerializer(menu_item).data
                        },
                        status=status.HTTP_200_OK
                    )
                else:
                    return Response(
                        {
                            'detail': 'Provide at least one of the following fields to update a menu item',
                            'fields': {
                                'title': 'A string no longer than 255 characters',
                                'price': 'A decimal number',
                                'inventory': 'A number between 0 and 65535'
                            }
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )
            else:
                return Response(
                    serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST
                )
            
        else:
            return Response(
                {
                    'detail': 'Only managers are allowed to access this endpoint'
                },
                status=status.HTTP_403_FORBIDDEN
            )
    
    def patch(self, request, id):
        user = request.user
        if user.groups.filter(name='Manager').exists():
            try:
                menu_item = models.Menu.objects.get(id=id)
            except ObjectDoesNotExist:
                return Response(
                    {
                        'detail': 'No item in the menu matches the id provided'
                    },
                    status=status.HTTP_404_NOT_FOUND
                )
            serializer = serializers.MenuItemDeserializer(data=request.data)
            if serializer.is_valid():
                validated_data = serializer.validated_data
                if len(validated_data) > 0:
                    for key, value in validated_data.items():
                        setattr(menu_item, key, value)
                    menu_item.save()
                    return Response(
                        {
                            'detail': 'The item in the menu has been updated successfully',
                            'menu_item': serializers.MenuSerializer(menu_item).data
                        },
                        status=status.HTTP_200_OK
                    )
                else:
                    return Response(
                        {
                            'detail': 'Provide at least one of the following fields to update a menu item',
                            'fields': {
                                'title': 'A string no longer than 255 characters',
                                'price': 'A decimal number',
                                'inventory': 'A number between 0 and 65535'
                            }
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )
            else:
                return Response(
                    serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST
                )
            
        else:
            return Response(
                {
                    'detail': 'Only managers are allowed to access this endpoint'
                },
                status=status.HTTP_403_FORBIDDEN
            )
        
    def delete(self, request, id):
        user = request.user
        if user.groups.filter(name='Manager').exists():
            try:
                menu_item = models.Menu.objects.get(id=id)
            except ObjectDoesNotExist:
                return Response(
                    {
                        'detail': 'No item in the menu matches the id provided'
                    },
                    status=status.HTTP_404_NOT_FOUND
                )
            menu_item.delete()
            return Response(
                {
                    'detail': 'The menu item has been deleted successfully'
                },
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {
                    'detail': 'Only managers are allowed to access this endpoint'
                },
                status=status.HTTP_403_FORBIDDEN
            )

class BookingAPI(APIView):
    authentication_classes = [TokenAuthentication]

    def get(self, request):
        user = request.user
        if user.groups.filter(name='Manager').exists():
            name = request.query_params.get('name')
            date = request.query_params.get('date')
            if name or date:
                if name and date:
                    bookings = models.Booking.objects.filter(Q(name__istartswith=name) & Q(date=date))
                    if bookings.exists():
                        serializer = serializers.BookingSerializer(bookings, many=True)
                        return Response(
                            serializer.data,
                            status=status.HTTP_200_OK
                        )
                    else:
                        return Response(
                            {
                                'detail': f'No bookings have been found in {date} containing the name {name}'
                            },
                            status=status.HTTP_404_NOT_FOUND
                        )
                elif name:
                    bookings = models.Booking.objects.filter(name__istartswith=name)
                    
                    if bookings.exists():
                        serializer = serializers.BookingSerializer(bookings, many=True)
                        return Response(
                            serializer.data,
                            status=status.HTTP_200_OK
                        )
                    else:
                        return Response(
                            {
                                'detail': f'No bookings have been found containing the name {name}'
                            },
                            status=status.HTTP_404_NOT_FOUND
                        )
                else:
                    bookings = models.Booking.objects.filter(date=date)
                    
                    if bookings.exists():
                        serializer = serializers.BookingSerializer(bookings, many=True)
                        return Response(
                            serializer.data,
                            status=status.HTTP_200_OK
                        )
                    else:
                        return Response(
                            {
                                'detail': f'No bookings have been found in {date}'
                            },
                            status=status.HTTP_404_NOT_FOUND
                        )
                        
            else:
                bookings = models.Booking.objects.all()
                return Response(
                    serializers.BookingSerializer(bookings, many=True).data,
                    status=status.HTTP_200_OK
                )
        else:
            now = timezone.now()
            if now.time() > datetime.time(hour=20):
                now = now.date() + datetime.timedelta(days=1)
            else:
                now = now.date()
            bookings = models.Booking.objects.filter(date__range=(now, now + datetime.timedelta(days=6)))
            available_bookings = {}
            for x in range(7):
                date = now + datetime.timedelta(days=x)
                available_bookings.update({date.strftime('%Y-%m-%d'): generate_available_times()})
            for book in bookings:
                available_bookings[book.date.strftime('%Y-%m-%d')].update({book.time.strftime('%H:%M'): 'NOT AVAILABLE'})
            return Response(
                {
                    'detail': 'BOOKING AVAILABILITY',
                    'bookings': available_bookings
                },
                status=status.HTTP_200_OK
            )

    
    def post(self, request):
        user = request.user
        if isinstance(user, AnonymousUser):
            return Response(
                {
                    'detail': 'User authentication is required to perform this action'
                },
                status=status.HTTP_403_FORBIDDEN
            )
        else:
            serializer = serializers.BookingSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            name = serializer.validated_data['name']
            no_of_guests = serializer.validated_data['no_of_guests']
            date = serializer.validated_data['date']
            time = serializer.validated_data['time']
            print(name)
            print(no_of_guests)
            print(date)
            print(time)
            book = models.Booking(
                name=name,
                no_of_guests=no_of_guests,
                date=date,
                time=time
            )
            try:
                book.full_clean()
                book.save()
            except:
                return Response(
                    {
                        'time': [
                            'This time is invalid'
                        ]
                    },
                    status=status.HTTP_403_FORBIDDEN
                )
            return Response(
                {
                    'detail': 'Your booking was created successfully',
                    'book': serializers.BookingSerializer(book).data
                },
                status=status.HTTP_201_CREATED
            )

class SingleBookingAPI(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        user = request.user
        if user.groups.filter(name='Manager').exists():
            try:
                booking = models.Booking.objects.get(id=id)
            except ObjectDoesNotExist:
                return Response(
                    {
                        'detail': 'No booking matches the id provided'
                    },
                    status=status.HTTP_404_NOT_FOUND
                )
            return Response(
                serializers.BookingSerializer(booking).data,
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {
                    'detail': 'Only managers are allowed to access this endpoint'
                },
                status=status.HTTP_403_FORBIDDEN
            )

    def delete(self, request, id):
        user = request.user
        if user.groups.filter(name='Manager').exists():
            try:
                book = models.Booking.objects.get(id=id)
            except ObjectDoesNotExist:
                return Response(
                    {
                        'detail': 'No booking matches the id provided'
                    },
                    status=status.HTTP_404_NOT_FOUND
                )
            book.delete()
            return Response(
                {
                    'detail': 'The booking has been deleted successfully'
                },
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {
                    'detail': 'Only managers are allowed to access this endpoint'
                },
                status=status.HTTP_403_FORBIDDEN
            )