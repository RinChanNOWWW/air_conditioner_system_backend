from django.db import models


# Create your models here.
class CommonLog(models.Model):
    room_id = models.IntegerField()
    date = models.DateField()
    detail_num = models.IntegerField(default=0)
    total_money = models.IntegerField(default=0)
    reach_target_times = models.IntegerField(default=0)
    scheduled_times = models.IntegerField(default=0)
    ac_use_times = models.IntegerField(default=0)
    change_temp_times = models.IntegerField(default=0)
    change_wind_times = models.IntegerField(default=0)
    online_time = models.IntegerField(default=0)

    class Meta:
        unique_together = ("room_id", "date")


class TargetTempLog(models.Model):
    room_id = models.IntegerField()
    date = models.DateField()
    target_temp = models.DecimalField(max_digits=3, decimal_places=1)
    duration = models.IntegerField(default=0)

    class Meta:
        unique_together = ("room_id", "date", "target_temp")


class WindLog(models.Model):
    room_id = models.IntegerField()
    date = models.DateField()
    wind = models.CharField(max_length=10)
    duration = models.IntegerField(default=0)

    class Meta:
        unique_together = ("room_id", "date", "wind")
