from django.shortcuts import render


## Teacher Edition
def all_room(request):
    return render(request, 'rooms.html')

def room_view(request):
    return render(request, 'room.html')

## Student Edition
def all_room_s(request):
    return render(request, 'rooms-student.html')

def room_view_s(request):
    return render(request, 'room-student.html')
