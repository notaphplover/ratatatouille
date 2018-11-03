from . import views
from django.urls import path

urlpatterns = [
    path('login/', views.UserAuth.as_view()),
    path('restaurants/', views.RestaurantList.as_view()),
]
