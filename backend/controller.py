from .service_list import serviceList
from .waiting_queue import waitingQueue
from .scheduler import schedule
from .pause_list import pauseList
from .models import TargetTempLog, WindLog
from datetime import date
from .room_list import roomList

# 轮询周期
interval = 5


def poll():
    print('Log: service list:', str(serviceList))
    print('Log: waiting queue:', waitingQueue.waiting_queue)

    for room in roomList.room_list:
        if serviceList.look_up(room.room_id) or waitingQueue.look_up(room.room_id) or pauseList.look_up(room.room_id):
            update_target_temp_log(room)

    for room in serviceList.service_list:
        room.set(
            online_time=room.online_time + interval
        )
        room.update_elec()
        room.update_money()
        update_wind_log(room)

    for item in pauseList.pause_list:
        room = item[0]
        if abs(room.target_temp - room.temp) > 1:
            new_request = {
                'room_id': room.room_id,
                'ac_status': item[1],
                'temp': room.temp,
                'target_temp': room.target_temp
            }
            waitingQueue.push(new_request)

    schedule()


def update_target_temp_log(room):
    obj, _ = TargetTempLog.objects.get_or_create(
        room_id=room.room_id,
        target_temp=room.target_temp,
        date=date.today()
    )
    obj.duration += interval
    obj.save()


def update_wind_log(room):
    obj, _ = WindLog.objects.get_or_create(
        room_id=room.room_id,
        date=date.today(),
        wind=room.ac_status
    )
    obj.duration += interval
    obj.save()
