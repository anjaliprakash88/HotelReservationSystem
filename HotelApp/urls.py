from django.urls import path
from . import views

urlpatterns = [
    path('', views.available_room, name="available_room"),
    path('reserve/', views.reserve_room, name="reserve_room"),
    path('check_available/', views.check_available, name='check_available'),
    path('book_room/', views.book_room, name='book_room'),


]
