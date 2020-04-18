from datetime import datetime
from .models import RoomStatus, RoomCheck, RoomLog
import air_conditioner_system.settings as st
from django.db.models import Q
from datetime import timedelta

class RoomStatusMixin():
    
    def clear_status(self, room: RoomStatus):
        room.ac_status = 'Off'
        room.temperature = '25.0'
        room.target_temp = '25.0'
        room.check_in_time = None
        room.last_change_time = None
        room.online_time = timedelta(0)
        room.electricity_now = 0
        room.save()

class RoomCheckMixin():

    def check_out(self, room: RoomCheck):
        room.check_out_time = datetime.now()
        room.save()



