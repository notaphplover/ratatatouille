from . import models, serializers
from django.contrib.auth import authenticate
from api.permissions import P_DISH_VIEW, P_RESTAURANT_ADD, P_RESTAURANT_VIEW
from rest_framework import permissions, status
from rest_framework.authtoken.models import Token
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

class DishList(APIView):
    def get(self, request: Request, restaurant: int, format=None):
        user_id = Token.objects.get(key=request.auth.key).user_id
        related_restaurants = models.UserRestaurantPermission.objects \
            .values(
                'restaurant__id'
            ) \
            .filter(
                user__id=user_id,
                permission__codename=P_DISH_VIEW,
                restaurant__id=restaurant
            )

        if 1 != len(related_restaurants):
            return Response(
                {'error': 'The user provided is not allowed to perform this operation'},
                status=status.HTTP_403_FORBIDDEN
            )

        dishes = models.Dish.objects.filter(restaurant__id=restaurant)
        serializer = serializers.DishSerializer(dishes, many=True)
        return Response(serializer.data)

class RestaurantList(APIView):
    """
    List all restaurants, or create a new restaurant.
    """
    def get(self, request: Request, format=None):
        user_id = Token.objects.get(key=request.auth.key).user_id
        related_restaurants = models.UserRestaurantPermission.objects\
            .values(
                'restaurant__id',
                'restaurant___created_at',
                'restaurant___updated_at',
                'restaurant__name'
            )\
            .filter(user__id=user_id, permission__codename=P_RESTAURANT_VIEW)

        restaurants = []
        for restaurant in related_restaurants:
            restaurants.append(models.Restaurant(
                id=restaurant['restaurant__id'],
                _created_at=restaurant['restaurant___created_at'],
                _updated_at=restaurant['restaurant___updated_at'],
                name=restaurant['restaurant__name']
            ))

        serializer = serializers.RestaurantSerializer(restaurants, many=True)
        return Response(serializer.data)

    def post(self, request: Request, format=None):
        user_id = Token.objects.get(key=request.auth.key).user_id
        user_permission = models.UserRestaurantPermission.objects\
            .values('permission__id')\
            .filter(
                permission__codename=P_RESTAURANT_ADD,
                user_id=user_id
            )

        if 1 != len(user_permission):
            return Response(
                {'error': 'The user provided is not allowed to perform this operation'},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = serializers.RestaurantSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserAuth(APIView):
    permission_classes = (permissions.AllowAny,)
    def post(self, request: Request, format=None):
        username = request.data.get('username')
        password = request.data.get('password')
        if username is None or password is None:
            return Response(
                {'error': 'Please provide both username and password'},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = authenticate(username=username, password=password)
        if not user:
            return Response(
                {'error': 'Invalid Credentials'},
                status=status.HTTP_404_NOT_FOUND
        )

        token, _ = Token.objects.get_or_create(user=user)
        return Response(
            {'token': token.key},
            status=status.HTTP_200_OK
        )
