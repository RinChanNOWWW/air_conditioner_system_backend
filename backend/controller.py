from .service_list import serviceList
from .waiting_queue import waitingQueue
from .scheduler import schedule
from .pause_list import pauseList
from .models import TargetTempLog, WindLog, CommonLog
from datetime import date
from .room_list import roomList

# 轮询周期
interval = 5


def poll():
    print('Log: service list:', str(serviceList))
    print('Log: waiting queue:', waitingQueue.waiting_queue)
    print('Log: pause list:', str(pauseList))

    for room in serviceList.service_list:
        room.set(
            online_time=room.online_time + interval
        )
        room.update_elec()
        room.update_money()
        update_online_time(room)
        update_wind_log(room)

    for room in roomList.room_list:
        if serviceList.look_up(room.room_id) or waitingQueue.look_up(room.room_id) or pauseList.look_up(room.room_id):
            update_target_temp_log(room)

    for request in waitingQueue.waiting_queue:
        request[1] += interval


    for item in pauseList.pause_list:
        room = item[0]
        # print(room.target_temp, room.temp)
        # print(room.target_temp - room.temp)
        if abs(room.temp - room.target_temp) >= 1:
            print('remove from pause list')
            new_request = {
                'room_id': room.room_id,
                'ac_status': item[1],
                'temp': room.temp,
                'target_temp': room.target_temp
            }
            pauseList.remove(room.room_id)
            print('remove from pause list')
            waitingQueue.push(new_request)
            print('add to waiting queue')

    schedule()


def update_online_time(room):
    obj, _ = CommonLog.objects.get_or_create(
        room_id=room.room_id,
        date=date.today()
    )
    obj.online_time += interval
    obj.save()


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
