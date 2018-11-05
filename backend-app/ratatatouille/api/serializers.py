from . import models
from rest_framework import serializers

class DishSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Dish
        fields = ('id', 'active', 'category', 'description', 'name', 'restaurant')

class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Restaurant
        fields = ('id', 'name')
