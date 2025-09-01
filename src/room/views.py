from django.shortcuts import render


def all_room(request):
    return render(request, 'rooms.html')

def room_view(request):
    return render(request, 'room.html')

