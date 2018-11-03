from django.contrib import admin

from .models import Dish, DishCategory, Menu, MenuDish, Restaurant, UserRestaurantPermission

admin.site.register(Dish)
admin.site.register(DishCategory)
admin.site.register(Menu)
admin.site.register(MenuDish)
admin.site.register(Restaurant)
admin.site.register(UserRestaurantPermission)
