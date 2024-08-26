from rest_framework import serializers
from restaurant.models import Menu, Booking

class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = '__all__'

class MenuItemDeserializer(serializers.Serializer):
    title = serializers.CharField(max_length=255, required=False)
    price = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    inventory = serializers.IntegerField(min_value=0, max_value=65535, required=False)

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'