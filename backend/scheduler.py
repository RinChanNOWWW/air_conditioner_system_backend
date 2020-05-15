from .models import RoomStatus
import air_conditioner_system.settings as st
from django.db.models import Q
from datetime import timedelta
from django.utils import timezone
from backend.models import RoomLog
from backend.taskqueue import taskQueue
from backend.serializers import RoomStatusUpdateSerializer
from backend.serializers import update_log

def scheduler(room_id: int, mode: str):
    if mode == 'Off':
        return True
    rooms_ac_on = RoomStatus.objects.filter(~Q(ac_status='Off'))
    room_now = RoomStatus.objects.get(room_id=room_id)
    room_now_old_ac_status = room_now.ac_status
    if room_now.ac_status != 'Off' or rooms_ac_on.count() < st.AC_MAX_NUM:
        return True
    rooms_ac_on = sorted(rooms_ac_on, key=lambda x: (st.PRIORITY[x.ac_status], -x.online_time))
    # print(rooms_ac_on)
    # print(room_now.ac_status, rooms_ac_on[0].ac_status)
    if st.PRIORITY[mode] >= st.PRIORITY[rooms_ac_on[0].ac_status]:
        print('Schedule Success')
        request = {
            'room_id': rooms_ac_on[0].room_id,
            'ac_status': rooms_ac_on[0].ac_status,
            'temperature': rooms_ac_on[0].temperature,
            'target_temp': rooms_ac_on[0].target_temp
        }
        old_status = rooms_ac_on[0].ac_status
        rooms_ac_on[0].ac_status = 'Off'
        rooms_ac_on[0].online_time = timedelta(0)
        rooms_ac_on[0].last_change_time = timezone.now()
        rooms_ac_on[0].save()
        old_request = RoomStatusUpdateSerializer(rooms_ac_on[0], data=request)
        taskQueue.push(old_request)
        update_log(rooms_ac_on[0], old_status)
        update_log(room_now, room_now_old_ac_status)
        return True
    return False

