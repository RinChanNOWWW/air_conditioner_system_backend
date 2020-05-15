from django.shortcuts import render
from django.utils import timezone
# from datetime import datetime
from django.db.models import Q
from django.db import models
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework import status
from .models import RoomLog, RoomCheck, RoomStatus
from .serializers import RoomLogSerializer, RoomCheckSerializer, RoomStatusSerializer, TimePeriodSerializer, RoomStatusUpdateSerializer
from .mixins import RoomStatusMixin, RoomCheckMixin
import air_conditioner_system.settings as st
from backend.scheduler import scheduler
from backend.taskqueue import taskQueue

class RoomStatusView(APIView):

    # 此方法只用于调试
    def get(self, request, format=None):
        room_id = request.query_params.get('room_id')
        # print(type(room_id))
        if room_id == None:
            serializer = RoomStatusSerializer(instance=RoomStatus.objects.all(), many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            try:
                room_id = int(room_id)
                room_status = RoomStatus.objects.get(room_id=room_id)
                # room_status.last_change_time = timezone.now()
                serializer = RoomStatusSerializer(instance=room_status)
                data = serializer.data
                return Response(data=data, status=status.HTTP_200_OK)
            except models.ObjectDoesNotExist:
                return Response(data={'error': 'No such room exists'}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, fromat=None):
        # print('OK0')
        # print(request.data.get('room_id'))
        room_id = request.data.get('room_id')
        request_ac_status = request.data.get('ac_status')
        room_status = RoomStatus.objects.get(room_id=room_id)
        ac_status_old = room_status.ac_status
        # print('OK1')
        serializer = RoomStatusUpdateSerializer(room_status, data=request.data)
        # print('OK2')
        if (serializer.is_valid()):
            if room_status.check_in_time != None:
                if room_status.ac_status != 'Off' or scheduler(int(room_id), request_ac_status):
                    taskQueue.remove(room_id)
                    room_status = serializer.save()
                    serializer = RoomStatusSerializer(instance=room_status)
                    return Response(data=serializer.data, status=status.HTTP_200_OK)
                else:
                    taskQueue.push(serializer)
                    room_status.ac_status = ac_status_old
                    room_status.save()
                    serializer = RoomStatusSerializer(instance=room_status)
                    return Response(data=serializer.data, status=status.HTTP_200_OK)
                # if scheduler(int(room_id), request_ac_status):
                #     room_status = serializer.save()
                #     # if room_status.ac_status != ac_status_old:
                #     #     log = {
                #     #         'room_id': room_status.room_id,
                #     #         'check_in_time': room_status.check_in_time,
                #     #         'timestamp': timezone.now(),
                #     #         'temperature': room_status.temperature,
                #     #         'ac_status': room_status.ac_status,
                #     #         'electricity_now': room_status.electricity_now
                #     #     }
                #     #     RoomLog.objects.create(**log)
                #     serializer = RoomStatusSerializer(instance=room_status)
                #     return Response(data=serializer.data, status=status.HTTP_200_OK)
                # else:
                #     taskQueue.push(serializer)
                #     room_status.ac_status = ac_status_old
                #     room_status.save()
                #     serializer = RoomStatusSerializer(instance=room_status)
                #     return Response(data=serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(data={'error': 'This room is not checked in'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data={"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


    def post(self, request, fromat=None):
        # 此方法用于用户开房以及管理员查看已开放的房间
        # 先判断身份是 客户 还是 空调管理员
        auth = request.data.get('auth')
        if auth == 'client':
            empty_rooms = RoomStatus.objects.filter(check_in_time=None)
            if empty_rooms.exists():
                # 能够开房
                room_status_object = empty_rooms.order_by('room_id')[0]
                room_id = room_status_object.room_id
                check_in_time = timezone.now()
                room_status_object.check_in_time = check_in_time
                room_status_object.last_change_time = check_in_time
                room_status_object.save()
                RoomCheck.objects.create(room_id=room_id, check_in_time=check_in_time)
                serializer = RoomStatusSerializer(instance=room_status_object)
                return Response(data=serializer.data, status=status.HTTP_200_OK)
            else:
                # 房间已满
                return Response(data={'error': 'All Room is full'}, status=status.HTTP_404_NOT_FOUND)
        elif auth == 'admin':
            check_in_rooms = RoomStatus.objects.filter(~Q(check_in_time=None))
            serializer = RoomStatusSerializer(instance=check_in_rooms, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(data={'error': 'Object Not Found'}, status=status.HTTP_404_NOT_FOUND)


class RoomCheckView(APIView):

    # 此方法用户酒店经理查询统计报表
    def post(self, request, format=None):
        time_period_serializer = TimePeriodSerializer(data=request.data)
        if (time_period_serializer.is_valid()):
            start_time = time_period_serializer.validated_data.get('start_time')
            end_time = time_period_serializer.validated_data.get('end_time')
            room_checks_among_the_period = RoomCheck.objects.filter(Q(check_in_time__gte=start_time) & (~Q(check_out_time__gt=end_time)))
            serializer = RoomCheckSerializer(instance=room_checks_among_the_period, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(data={"errors": time_period_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class RoomLogView(APIView, RoomStatusMixin, RoomCheckMixin):

    def get(self, request, fromat=None):
        room_id = request.query_params.get('room_id')
        # print(type(room_id))
        if room_id != None:
            try:
                room_id = int(room_id)
                # print(room_id)
                room_status = RoomStatus.objects.get(room_id=room_id)
                if room_status.ac_status == 'Off':
                    check_in_time = room_status.check_in_time
                    # print('OK')
                    self.clear_status(room_status)
                    room_check = RoomCheck.objects.get(room_id=room_id, check_in_time=check_in_time)
                    # print(check_in_time)
                    self.check_out(room_check)
                    room_logs = RoomLog.objects.filter(room_id=room_id, check_in_time=check_in_time)
                    serilizer = RoomLogSerializer(instance=room_logs, many=True)
                    data = serilizer.data
                    return Response(data=data, status=status.HTTP_200_OK)
                else:
                    return Response(data={'error': 'ac is not off'}, status=status.HTTP_404_NOT_FOUND)
            except models.ObjectDoesNotExist:
                return Response(data={'error': 'No such room checked in'}, status=status.HTTP_404_NOT_FOUND)
        return Response(data={'error': 'No room id'}, status=status.HTTP_404_NOT_FOUND)

    