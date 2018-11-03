from django.test import Client, TestCase
from rest_framework import status

class RestaurantTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        # Call the API
        login_response_json = self.client.post(
            '/api/v1/login/',
            {'username':'super', 'password': 'super'}
        ).json()
        self.token = login_response_json['token']
        self.token_client = Client(HTTP_AUTHORIZATION='Bearer ' + self.token)

    def testApiGetRestaurantsReturnsRestaurantsOwnedByTheUser(self):

        restaurants_response = self.token_client.get(
            '/api/v1/restaurants/'
        )

        restaurants_json = restaurants_response.json()

        self.assertLess(0, len(restaurants_json))
        self.assertEqual(status.HTTP_200_OK, restaurants_response.status_code)
