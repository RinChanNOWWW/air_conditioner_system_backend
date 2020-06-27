from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework import status
from rest_framework.response import Response
from django.db.models import Sum
from .ac_settings import acSettings
from .room_info import RoomInfo
from .room_list import roomList
from .service_list import serviceList
from .waiting_queue import waitingQueue
from .serializers import *
from .scheduler import schedule
from .pause_list import pauseList
from .models import CommonLog, WindLog, TargetTempLog
from datetime import date, datetime
import pandas as pd


# Create your views here.
# admin apis
class SetUp(APIView):

    def get(self, request):
        return Response({'Info': 'This METHOD is not defined'}, status=status.HTTP_200_OK)

    def post(self, request: Request, format=None):
        content = request.data
        # 进行默认设置初始化
        acSettings.set_room_num(content.get('room_num'))
        acSettings.set_temp_period({
            'min': content.get('min_temp'),
            'max': content.get('max_temp')
        })
        acSettings.set_mode(content.get('mode'))
        acSettings.set_default_temp(content.get('default_temp'))
        acSettings.set_max_serve_num(content.get('max_serve_num'))
        acSettings.set_power_price(content.get('price'))
        acSettings.set_wind_power(content.get('low'), content.get('medium'), content.get('high'))
        while roomList.length() != 0:
            roomList.remove_room()
        # 进行房间初始化
        for i in range(1, acSettings.room_num + 1):
            room = RoomInfo(room_id=i, target_temp=acSettings.default_temp, temp=acSettings.default_temp)
            roomList.add_room(room)
        print('Log: init', roomList.length(), 'rooms')
        return Response(status=status.HTTP_200_OK)


class Monitor(APIView):

    def get(self, request, format=None):
        serializer = RoomInfoSerializer(roomList.room_list, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


# user apis
class CheckIn(APIView):

    def get(self, request: Request, format=None):
        for room in roomList.room_list:
            if not room.is_checked():
                room.check_in()
                serializer = RoomInfoSerializer(room)
                data = serializer.data
                data['temp_min'] = acSettings.temp_period['min']
                data['temp_max'] = acSettings.temp_period['max']
                return Response(data=data, status=status.HTTP_200_OK)
        return Response(data={'Error': 'No empty room.'}, status=status.HTTP_404_NOT_FOUND)


class HeartBeat(APIView):

    def post(self, request: Request, format=None):
        req = HeartBeatSerializer(data=request.data)
        content = None
        if req.is_valid():
            content = req.validated_data
        else:
            return Response({'Error': 'Data can not be serialized.'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        room = roomList.get_room(content['room_id'])
        if room.is_checked():
            room.set(temp=content['temp'])
            if room.temp == room.target_temp and room.ac_status != 'off':
                obj, _ = CommonLog.objects.get_or_create(room_id=room.room_id, date=date.today())
                obj.reach_target_times += 1
                obj.save()
                if serviceList.look_up(room.room_id):
                    serviceList.remove(room.room_id)
                if waitingQueue.look_up(room.room_id):
                    waitingQueue.remove(room.room_id)
                old_ac_status = room.ac_status
                room.set(ac_status='off', online_time=0)
                room.add_detail()
                pauseList.append(room, old_ac_status)
        response = RoomInfoSerializer(room)
        return Response(response.data, status=status.HTTP_200_OK)


class SetMode(APIView):

    def post(self, request: Request, format=None):
        serializer = SetModeRequestSerializer(data=request.data)
        content = None
        if serializer.is_valid():
            content = serializer.validated_data
        else:
            return Response({'Error': 'Data can not be serialized.'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        room = roomList.get_room(content['room_id'])
        old_ac_status = ''
        if room is not None and room.is_checked():
            old_ac_status = room.ac_status
            if serviceList.look_up(room.room_id):
                serviceList.remove(room.room_id)
                print('Log: remove room ', room.room_id, ' from service list.')
            if waitingQueue.look_up(room.room_id):
                waitingQueue.remove(room.room_id)
                print('Log: remove room', room.room_id, ' from waiting list.')
            if pauseList.look_up(room.room_id):
                pauseList.remove(room.room_id)
                print('Log: remove room', room.room_id, ' from pause list.')

            room.set(target_temp=content['target_temp'])
            print(room.ac_status, content['ac_status'])
            if old_ac_status == content['ac_status']:
                print('set target temp success')
                serializer = RoomInfoSerializer(room)
                return Response(serializer.data, status=status.HTTP_200_OK)

            if content['ac_status'] == 'off':
                room.set(ac_status='off', online_time=0)
                room.add_detail()
                print('Log: turn off room ', room.room_id)
            else:
                waitingQueue.push(content)
                print('Log: push room ', room.room_id, ' into waiting queue.')
            # 参数为 1 表示立即调度
            schedule(1)
            serializer = RoomInfoSerializer(room)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'Error': 'This room is not checked in or not exist.'}, status=status.HTTP_404_NOT_FOUND)


# front apis
class Detail(APIView):
    def post(self, request: Request, format=None):
        room_id = request.data.get('room_id')
        room = roomList.get_room(room_id)
        if room is not None and room.is_checked():
            details = room.get_details()
            serializer = DetailSerializer(details, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'Error': 'This room is not checked in.'}, status=status.HTTP_404_NOT_FOUND)


class CheckOut(APIView):
    def post(self, request: Request, format=None):
        room_id = request.data.get('room_id')
        room = roomList.get_room(room_id)
        if room is not None and room.is_checked():
            bill = {
                'room_id': room_id,
                'total_money': room.total_money,
                'checkin_time': room.checkin_time,
                'checkout_time': datetime.now(),
            }
            print('ready to check out')
            room.check_out()
            print('checked out')
            return Response(data=bill, status=status.HTTP_200_OK)
        else:
            return Response({'Error': 'This room is not checked in.'}, status=status.HTTP_404_NOT_FOUND)


# manager apis
class DailyReport(APIView):
    def post(self, request: Request, format=None):
        d = request.data.get('date').split('-')
        request_date = date(int(d[0]), int(d[1]), int(d[2]))
        report_list = list(CommonLog.objects.filter(date=request_date).values())
        for report in report_list[::-1]:
            if report['scheduled_times'] == 0:
                report_list.remove(report)
        if len(report_list) == 0:
            serializer = DailyReportSerializer(report_list, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        target_df = pd.DataFrame(list(TargetTempLog.objects.filter(date=request_date).values()))
        target_group = target_df.groupby('room_id')
        target_group = target_group['duration'].max()
        target = pd.merge(target_df, target_group, on=['room_id', 'duration'])
        wind_df = pd.DataFrame(list(WindLog.objects.filter(date=request_date).values()))
        wind_group = wind_df.groupby('room_id')
        wind_group = wind_group['duration'].max()
        wind = pd.merge(wind_df, wind_group, on=['room_id', 'duration'])
        for r in report_list:
            r['most_use_target_temp'] = int(
                target[target['room_id'] == r['room_id']]['target_temp'].values[0]
            )
            r['most_use_wind'] = str(
                wind[wind['room_id'] == r['room_id']]['wind'].values[0]
            )
        serializer = DailyReportSerializer(report_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class OtherReport(APIView):
    def post(self, request: Request, format=None):
        start_date = request.data.get('start_date').split('-')
        end_date = request.data.get('end_date').split('-')
        request_start_date = date(int(start_date[0]), int(start_date[1]), int(start_date[2]))
        request_end_date = date(int(end_date[0]), int(end_date[1]), int(end_date[2]))
        report_list = list(
            CommonLog.objects.filter(date__range=(request_start_date, request_end_date)).values('room_id')
            .annotate(detail_num_sum=Sum('detail_num'),
                      total_money_sum=Sum('total_money'),
                      reach_target_times_sum=Sum('reach_target_times'),
                      scheduled_times_sum=Sum('scheduled_times'),
                      ac_use_times_sum=Sum('ac_use_times'),
                      change_temp_times_sum=Sum('change_temp_times'),
                      change_wind_times_sum=Sum('change_wind_times'),
                      online_time_sum=Sum('online_time')))

        serializer = OtherReportSerializer(report_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
