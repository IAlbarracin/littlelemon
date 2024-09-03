from rest_framework import serializers
from restaurant.models import Menu, Booking
from django.contrib.auth.models import User

class GroupsSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()

class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    groups = GroupsSerializer(read_only=True, many=True)

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'password',
            'email',
            'groups'
        ]

class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = '__all__'

class MenuItemDeserializer(serializers.Serializer):
    title = serializers.CharField(max_length=255, required=False)
    price = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    inventory = serializers.IntegerField(min_value=0, max_value=65535, required=False)

class BookingSerializer(serializers.ModelSerializer):
    time = serializers.TimeField(format="%H:%M")

    class Meta:
        model = Booking
        fields = [
            'id',
            'name',
            'no_of_guests',
            'date',
            'time',
        ]