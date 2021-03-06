from .service_list import serviceList
from .waiting_queue import waitingQueue
from .room_list import roomList
from .ac_settings import priority, acSettings
from .models import CommonLog, TargetTempLog, WindLog
from datetime import date
import backend.controller


def schedule(condition=0):
    if waitingQueue.length() > 0:
        request = waitingQueue.front()
        waited_time = waitingQueue.get_front_waited_time()
        if serviceList.length() < acSettings.max_serve_num:
            new_service_room = roomList.get_room(request['room_id'])
            old_ac_status = new_service_room.ac_status
            new_service_room.set(
                ac_status=request['ac_status'],
                # temp=request['temp'],
                target_temp=request['target_temp']
            )
            new_service_room.add_detail()
            serviceList.append(new_service_room)
            obj, _ = CommonLog.objects.get_or_create(
                room_id=new_service_room.room_id,
                date=date.today()
            )
            obj.scheduled_times += 1
            if old_ac_status == 'off':
                obj.ac_use_times += 1
            obj.save()
            waitingQueue.pop()
        else:
            lowest_room = serviceList.get_lowest_room()
            if condition == 1 and priority[request['ac_status']] > priority[lowest_room.ac_status]:
                new_request = {
                    'room_id': lowest_room.room_id,
                    'ac_status': lowest_room.ac_status,
                    'temp': lowest_room.temp,
                    'target_temp': lowest_room.target_temp
                }
                serviceList.remove(lowest_room.room_id)
                lowest_room.add_detail()
                waitingQueue.push(new_request)
                new_service_room = roomList.get_room(request['room_id'])
                old_ac_status = new_service_room.ac_status
                new_service_room.set(
                    ac_status=request['ac_status'],
                    # temp=request['temp'],
                    target_temp=request['target_temp']
                )
                new_service_room.add_detail()
                serviceList.append(new_service_room)
                obj, _ = CommonLog.objects.get_or_create(
                    room_id=new_service_room.room_id,
                    date=date.today()
                )
                obj.scheduled_times += 1
                if old_ac_status == 'off':
                    obj.ac_use_times += 1
                obj.save()
                waitingQueue.pop()
            elif priority[request['ac_status']] > priority[lowest_room.ac_status] or \
                (priority[request['ac_status']] == priority[lowest_room.ac_status] and
                 waited_time >= 2 * backend.controller.interval and
                 lowest_room.online_time >= 2 * backend.controller.interval):
                new_request = {
                    'room_id': lowest_room.room_id,
                    'ac_status': lowest_room.ac_status,
                    'temp': lowest_room.temp,
                    'target_temp': lowest_room.target_temp
                }
                serviceList.remove(lowest_room.room_id)
                lowest_room.add_detail()
                waitingQueue.push(new_request)
                new_service_room = roomList.get_room(request['room_id'])
                old_ac_status = new_service_room.ac_status
                new_service_room.set(
                    ac_status=request['ac_status'],
                    # temp=request['temp'],
                    target_temp=request['target_temp']
                )
                new_service_room.add_detail()
                serviceList.append(new_service_room)
                obj, _ = CommonLog.objects.get_or_create(
                    room_id=new_service_room.room_id,
                    date=date.today()
                )
                obj.scheduled_times += 1
                if old_ac_status == 'off':
                    obj.ac_use_times += 1
                obj.save()
                waitingQueue.pop()
    print('Schedule Done.')
