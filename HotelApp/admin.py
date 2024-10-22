from django.contrib import admin
from .models import Roomcategory, Room, Reservation, Specialrate


admin.site.register(Roomcategory)
admin.site.register(Room)
admin.site.register(Reservation)
admin.site.register(Specialrate)
