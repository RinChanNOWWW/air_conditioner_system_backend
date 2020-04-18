from rest_framework import serializers
from .models import RoomCheck, RoomStatus, RoomLog
from datetime import timedelta
from django.utils import timezone
import air_conditioner_system.settings as st

class RoomCheckSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomCheck
        fields = '__all__'

class RoomStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomStatus
        fields = '__all__'

class RoomLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomLog
        fields = '__all__'

class TimePeriodSerializer(serializers.Serializer):
    start_time = serializers.DateTimeField()
    end_time = serializers.DateTimeField()

class RoomStatusUpdateSerializer(serializers.Serializer):
    
    room_id = serializers.IntegerField()
    ac_status = serializers.CharField()
    temperature = serializers.DecimalField(max_digits=3, decimal_places=1)
    target_temp = serializers.DecimalField(max_digits=3, decimal_places=1)
    # electricity_now = serializers.IntegerField()
    # timestamp = serializers.DateTimeField()
    # last_change_time = serializers.DateTimeField()

    def create(self, validated_data):
        return RoomStatus.objects.create(**validated_data)

    def update(self, instance: RoomStatus, validated_data):
        now = timezone.now()
        interval = now - instance.last_change_time
        if interval.seconds >= 60:
            instance.electricity_now += (interval.seconds // 60) * st.ELEC[str(instance.ac_status)]
        else:
            instance.electricity_now += st.ELEC[str(instance.ac_status)]
        room_check = RoomCheck.objects.get(room_id=instance.room_id, check_in_time=instance.check_in_time)
        room_check.electricity_now = instance.electricity_now
        room_check.save()
        # instance.room_id = validated_data.get('room_id', instance.room_id)
        instance.temperature = validated_data.get('temperature', instance.temperature)
        # instance.electricity_now = validated_data.get('electricity_now', instance.electricity_now)
        instance.target_temp = validated_data.get('target_temp', instance.target_temp)
        instance.ac_status = validated_data.get('ac_status', instance.ac_status)
        # instance.online_time += timezone.now() - instance.last_change_time
        if instance.temperature == instance.target_temp:
            print('Off')
            instance.ac_status = 'Off'
            instance.online_time = timedelta(0)
        instance.last_change_time = now
        instance.save()
        print("Update Room", instance.room_id)
        return instance
