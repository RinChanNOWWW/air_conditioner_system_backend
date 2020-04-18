from .models import RoomStatus, RoomCheck
from django.db.models import Q
from datetime import datetime, timezone, timedelta
import air_conditioner_system.settings as settings
from django.utils import timezone

def poll():
    room_list = RoomStatus.objects.filter(~Q(ac_status='Off'))
    for room in room_list:
        now = timezone.now()
        print(now)
        print("Room:", room.room_id, "Temp:", room.temperature, "Elec:", room.electricity_now)
        interval = now - room.last_change_time
        room.online_time += timedelta(seconds=1)
        if interval.seconds >= 60:
            room.electricity_now += (interval.seconds // 60) * settings.ELEC[str(room.ac_status)]
            room_check = RoomCheck.objects.get(room_id=room.room_id, check_in_time=room.check_in_time)
            room_check.electricity_now = room.electricity_now
            room_check.save()

            room.last_change_time = now
        room.save()