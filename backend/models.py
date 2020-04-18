from django.db import models
from datetime import timedelta

# Create your models here.
class RoomStatus(models.Model):
    room_id = models.IntegerField(primary_key=True)
    ac_status = models.CharField(max_length=10, default='Off')
    temperature = models.DecimalField(max_digits=3, decimal_places=1, default=25.0)
    target_temp = models.DecimalField(max_digits=3, decimal_places=1, default=25.0)
    check_in_time = models.DateTimeField(blank=True, null=True)
    last_change_time = models.DateTimeField(blank=True, null=True)
    online_time = models.DurationField(default=timedelta(0))
    # 当前耗电
    electricity_now = models.IntegerField(default=0)

    def __str__(self):
        return 'room_id: {room_id}, ac: {ac}, temp: {temp}, check in time: {check_in}, elec: {elec}'.format(room_id=self.room_id, ac=self.ac_status, temp=self.temperature, check_in=self.check_in_time, elec=self.electricity_now)


class RoomCheck(models.Model):
    room_id = models.IntegerField()
    check_in_time = models.DateTimeField()
    check_out_time = models.DateTimeField(blank=True, null=True)
    # 开房到现在累计耗电
    electricity_now = models.IntegerField(default=0)

    class Meta:
        unique_together = ("room_id", "check_in_time")

class RoomLog(models.Model):
    room_id = models.IntegerField()
    check_in_time = models.DateTimeField()
    timestamp = models.DateTimeField()
    temperature = models.DecimalField(max_digits=3, decimal_places=1)
    ac_status = models.CharField(max_length=10)
    # 开房到现在累计耗电
    electricity_now = models.IntegerField(default=0)
    
    class Meta:
        unique_together = ("room_id", "check_in_time", "timestamp")
