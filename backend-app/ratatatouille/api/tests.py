from django.contrib.auth.models import Permission, User
from django.test import Client, TestCase
from api.models import Dish, Restaurant, UserRestaurantPermission
from api.permissions import P_DISH_VIEW, P_RESTAURANT_VIEW
from rest_framework import status

class RestaurantTestCase(TestCase):

    def alternativeDishSearch(self, user: User, restaurant: Restaurant):
        dishes = []

        for user_permission in self.user_permissions.filter(
            restaurant__id=restaurant.id,
            user__id=user.id
        ):
            if P_DISH_VIEW == user_permission.permission.codename:
                for dish in self.dishes.filter(restaurant__id=restaurant.id):
                    dishes.append(dish)
                break

        return dishes

    def alternativeRestaurantSearch(self, user: User):
        restaurants = []
        for user_permission in self.user_permissions.filter(user__id=user.id):
            if P_RESTAURANT_VIEW == user_permission.permission.codename:
                restaurants.append(user_permission.restaurant)
                break

        return restaurants

    @classmethod
    def setUpTestData(cls):
        cls.dishes = Dish.objects.all()
        cls.permissions = Permission.objects.all()
        cls.restaurants = Restaurant.objects.all()
        cls.users = User.objects.all()
        cls.user_permissions = UserRestaurantPermission.objects.all()

    def setUp(self):
        self.client = Client()
        self.super_user = User.objects.get(username='super')
        # Call the API
        super_response_json = self.client.post(
            '/api/v1/login/',
            {'username':'super', 'password': 'super'}
        ).json()
        self.super_token = super_response_json['token']
        self.super_client = Client(HTTP_AUTHORIZATION='Bearer ' + self.super_token)

        loser_response_json = self.client.post(
            '/api/v1/login/',
            {'username': 'loser', 'password': 'loser'}
        ).json()
        self.loser_token = loser_response_json['token']
        self.loser_client = Client(HTTP_AUTHORIZATION='Bearer ' + self.loser_token)

    def testApiGetDishesDoesNotReturnDishesToNotGrantedUsers(self):
        user_restaurants = self.alternativeRestaurantSearch(self.super_user)

        for restaurant in user_restaurants:
            dishes_response = self.loser_client.get(
                '/api/v1/dishes/' + str(restaurant.id) + '/'
            )

            self.assertEqual(status.HTTP_403_FORBIDDEN, dishes_response.status_code)

    def testApiGetDishesReturnsDishesOfTheRestaurant(self):
        user_restaurants = self.alternativeRestaurantSearch(self.super_user)

        for restaurant in user_restaurants:
            dishes_response = self.super_client.get(
                '/api/v1/dishes/' + str(restaurant.id) + '/'
            )

            dishes_json = dishes_response.json()
            alternative_dishes = self.alternativeDishSearch(self.super_user, restaurant)

            self.assertEqual(status.HTTP_200_OK, dishes_response.status_code)
            self.assertEqual(len(alternative_dishes), len(dishes_json))

            for dish_json in dishes_json:
                self.assertTrue(any(dish_json['id'] == o.id for o in alternative_dishes))

    def testApiGetRestaurantsReturnsRestaurantsOwnedByTheUser(self):
        restaurants_response = self.super_client.get(
            '/api/v1/restaurants/'
        )

        restaurants_json = restaurants_response.json()
        alternative_restaurants = self.alternativeRestaurantSearch(self.super_user)

        self.assertEqual(status.HTTP_200_OK, restaurants_response.status_code)
        self.assertEqual(len(alternative_restaurants), len(restaurants_json))

        for restaurant_json in restaurants_json:
            self.assertTrue(any(restaurant_json['id'] == o.id for o in alternative_restaurants))
