from django.db import models


class Roomcategory(models.Model):
    name = models.CharField(max_length=100)
    base_price = models.DecimalField(max_digits=10, decimal_places=2)


class Room(models.Model):
    room_no = models.CharField(max_length=500)
    category = models.ForeignKey(Roomcategory, on_delete=models.CASCADE)
    is_available = models.BooleanField(default=True)


class Reservation(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    customer_name = models.CharField(max_length=225)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)


class Specialrate(models.Model):
    room_category = models.ForeignKey(Roomcategory, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    rate_multiplier = models.DecimalField(max_digits=10, decimal_places=2)

