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
        self.user = User.objects.get(username='super')
        # Call the API
        login_response_json = self.client.post(
            '/api/v1/login/',
            {'username':'super', 'password': 'super'}
        ).json()
        self.token = login_response_json['token']
        self.token_client = Client(HTTP_AUTHORIZATION='Bearer ' + self.token)

    def testApiGetDishesReturnsDishesOfTheRestaurant(self):
        user_restaurants = self.alternativeRestaurantSearch(self.user)

        for restaurant in user_restaurants:
            dishes_response = self.token_client.get(
                '/api/v1/dishes/' + str(restaurant.id) + '/'
            )

            dishes_json = dishes_response.json()
            alternative_dishes = self.alternativeDishSearch(self.user, restaurant)

            self.assertEqual(status.HTTP_200_OK, dishes_response.status_code)
            self.assertEqual(len(alternative_dishes), len(dishes_json))

            for dish_json in dishes_json:
                self.assertTrue(any(dish_json['id'] == o.id for o in alternative_dishes))

    def testApiGetRestaurantsReturnsRestaurantsOwnedByTheUser(self):
        restaurants_response = self.token_client.get(
            '/api/v1/restaurants/'
        )

        restaurants_json = restaurants_response.json()
        alternative_restaurants = self.alternativeRestaurantSearch(self.user)

        self.assertEqual(status.HTTP_200_OK, restaurants_response.status_code)
        self.assertEqual(len(alternative_restaurants), len(restaurants_json))

        for restaurant_json in restaurants_json:
            self.assertTrue(any(restaurant_json['id'] == o.id for o in alternative_restaurants))
