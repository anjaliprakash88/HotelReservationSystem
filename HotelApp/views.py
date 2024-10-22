from django.shortcuts import render, redirect
from .models import Room, Reservation, Roomcategory, Specialrate
from datetime import datetime, timedelta
from django.http import HttpResponse


def available_room(request):
    rooms = Room.objects.filter(is_available=True)
    context = {'rooms': rooms}
    return render(request, 'available_room.html', context)


def check_available(request):
    if request.method == 'GET':
        check_in = request.GET.get('check_in')
        check_out = request.GET.get('check_out')
        category_id = request.GET.get('category')

        available_rooms = Room.objects.all()

        if check_in and check_out:
            check_in_dt = datetime.strptime(check_in, '%Y-%m-%d').date()
            check_out_dt = datetime.strptime(check_out, '%Y-%m-%d').date()

            if category_id:
                available_rooms = available_rooms.filter(category__id=category_id)

            overlapping_reservations = Reservation.objects.filter(room__in=available_rooms,
                                                                  start_date__lt=check_out_dt,
                                                                  end_date__gt=check_in_dt)
            available_rooms = available_rooms.exclude(id__in=overlapping_reservations.values('room_id'))

        categories = Roomcategory.objects.all()

        context = {
            'available_rooms': available_rooms,
            'categories': categories
        }
        return render(request, 'check_available.html', context)


def reserve_room(request):
    if request.method == 'POST':
        room_id = request.POST.get('room')
        customer_name = request.POST.get('customer_name')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()

        room = Room.objects.get(id=room_id)

        overlap_reservations = Reservation.objects.filter(
            room=room, start_date__lt=end_date, end_date__gt=start_date
        )

        if overlap_reservations.exists():
            return HttpResponse("Room already booked")

        total_price = 0
        current_date = start_date

        while current_date <= end_date:
            base_price = room.category.base_price

            special_rate = Specialrate.objects.filter(
                room_category=room.category,
                start_date__lte=current_date,
                end_date__gte=current_date
            ).first()

            if special_rate:
                base_price *= special_rate.rate_multiplier

            total_price += base_price

            current_date += timedelta(days=1)

        reservation = Reservation.objects.create(
            room=room,
            customer_name=customer_name,
            start_date=start_date,
            end_date=end_date,
            total_price=total_price
        )

        room.is_available = False
        room.save()

        return redirect('available_room')

    elif request.method == 'GET':
        rooms = Room.objects.filter(is_available=True)
        context = {'rooms': rooms}
        return render(request, 'available_room.html', context)


def book_room(request):
    if request.method == 'POST':
        room_id = request.POST.get('room')
        customer_name = request.POST.get('customer_name')
        check_in = request.POST.get('check_in')
        check_out = request.POST.get('check_out')

        check_in_date = datetime.strptime(check_in, '%Y-%m-%d').date()
        check_out_date = datetime.strptime(check_out, '%Y-%m-%d').date()

        room = Room.objects.get(id=room_id)

        overlapping_reservations = Reservation.objects.filter(room=room, start_date__lt=check_out_date,
                                                              end_date__gt=check_in_date)

        if overlapping_reservations.exists():
            return HttpResponse("Room is already booked for the selected dates.")

        total_price = 0
        current_date = check_in_date

        while current_date <= check_out_date:
            base_price = room.category.base_price
            special_rate = Specialrate.objects.filter(
                room_category=room.category,
                start_date__lte=current_date,
                end_date__gte=current_date
            ).first()

            if special_rate:
                base_price *= special_rate.rate_multiplier

            total_price += base_price
            current_date += timedelta(days=1)

        reservation = Reservation.objects.create(
            room=room,
            customer_name=customer_name,
            start_date=check_in_date,
            end_date=check_out_date,
            total_price=total_price
        )

        room.is_available = False
        room.save()

        return HttpResponse(f"Room booked successfully! Total Price: {total_price}")

    return redirect('check_available')
