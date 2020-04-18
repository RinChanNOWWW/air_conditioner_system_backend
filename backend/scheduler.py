from .models import RoomStatus
import air_conditioner_system.settings as st
from django.db.models import Q
from datetime import timedelta
from django.utils import timezone

def scheduler(room_id: int, mode: str):
    rooms_ac_on = RoomStatus.objects.filter(~Q(ac_status='Off'))
    room_now = RoomStatus.objects.get(room_id=room_id)
    if room_now.ac_status != 'Off' or rooms_ac_on.count() < st.AC_MAX_NUM:
        return True
    rooms_ac_on = sorted(rooms_ac_on, key=lambda x: (st.PRIORITY[x.ac_status], -x.online_time))
    # print(rooms_ac_on)
    # print(room_now.ac_status, rooms_ac_on[0].ac_status)
    if st.PRIORITY[mode] >= st.PRIORITY[rooms_ac_on[0].ac_status]:
        print('Schedule Success')
        rooms_ac_on[0].ac_status = 'Off'
        rooms_ac_on[0].online_time = timedelta(0)
        rooms_ac_on[0].last_change_time = timezone.now()
        rooms_ac_on[0].save()
        return True
    return False