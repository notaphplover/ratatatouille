from django.contrib.auth.models import User, Permission
from django.utils import timezone

from django.db import models

class RatatatouilleModel(models.Model):
    _created_at = models.DateTimeField(None, default=timezone.now)
    _updated_at = models.DateTimeField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self._updated_at = timezone.now()
        super().save(force_insert, force_update, using, update_fields)

    class Meta:
        abstract = True

class Restaurant(RatatatouilleModel):
    name = models.CharField(max_length=255)

class DishCategory(RatatatouilleModel):
    short_name = models.CharField(max_length=64)

class Dish(RatatatouilleModel):
    active = models.BooleanField()
    category = models.ForeignKey(DishCategory, on_delete=models.CASCADE)
    description = models.TextField()
    name = models.CharField(max_length=255)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)

class Menu(RatatatouilleModel):
    active = models.BooleanField()
    name = models.CharField(max_length=255)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)

class MenuDish(RatatatouilleModel):
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('dish', 'menu'),)

class UserRestaurantPermission(RatatatouilleModel):
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('permission', 'restaurant', 'user'),)