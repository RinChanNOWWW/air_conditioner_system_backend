from django import setup
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'air_conditioner_system.settings')
setup()

from backend.models import RoomStatus
room_id = 101
while room_id <= 510:
    RoomStatus.objects.create(room_id=room_id)
    print('Room ', room_id, ' created')
    room_id += 1
    if room_id % 100 == 11:
        room_id += 100
        room_id -= 10
