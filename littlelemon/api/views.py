from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from restaurant import models
from . import serializers
from django.core.exceptions import ObjectDoesNotExist

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
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        if user.groups.filter(name='Manager').exists():
            params = request.query_params

        else:
            pass