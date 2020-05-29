from rest_framework import serializers


class RoomInfoSerializer(serializers.Serializer):
    room_id = serializers.IntegerField()
    ac_status = serializers.CharField(max_length=10)
    temp = serializers.DecimalField(max_digits=3, decimal_places=1)
    target_temp = serializers.DecimalField(max_digits=3, decimal_places=1)
    elec = serializers.IntegerField()
    online_time = serializers.IntegerField
    checked = serializers.BooleanField()
    total_money = serializers.IntegerField()


class SetModeRequestSerializer(serializers.Serializer):
    room_id = serializers.IntegerField()
    ac_status = serializers.CharField(max_length=10)
    temp = serializers.DecimalField(max_digits=3, decimal_places=1)
    target_temp = serializers.DecimalField(max_digits=3, decimal_places=1)


class DetailSerializer(serializers.Serializer):
    room_id = serializers.IntegerField()
    ac_status = serializers.CharField(max_length=10)
    temp = serializers.DecimalField(max_digits=3, decimal_places=1)
    target_temp = serializers.DecimalField(max_digits=3, decimal_places=1)
    elec = serializers.IntegerField()
    total_money = serializers.IntegerField()
    timestamp = serializers.DateTimeField()


class HeartBeatSerializer(serializers.Serializer):
    room_id = serializers.IntegerField()
    ac_status = serializers.CharField(max_length=10)
    temp = serializers.DecimalField(max_digits=3, decimal_places=1)
    target_temp = serializers.DecimalField(max_digits=3, decimal_places=1)


class ReportSerializer(serializers.Serializer):
    room_id = serializers.IntegerField()
    date = serializers.DateField()
    most_use_target_temp = serializers.DecimalField(max_digits=3, decimal_places=1)
    most_use_wind = serializers.CharField(max_length=10)
    reach_target_times = serializers.IntegerField()
    scheduled_times = serializers.IntegerField()
    detail_num = serializers.IntegerField()
    total_money = serializers.IntegerField()
