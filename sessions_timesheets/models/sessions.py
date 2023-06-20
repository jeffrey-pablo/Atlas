import datetime

from django.db import models
from .time_sheets import TimeSheet


class Session(models.Model):
    time_in = models.DateTimeField('Time In', blank=True)
    time_out = models.DateTimeField('Time Out', blank=True,null=True)
    session_time = models.DurationField('Session Time',blank=True,null=True)
    time_sheet = models.ForeignKey(TimeSheet,on_delete=models.PROTECT,related_name='sessions')
    user = models.ForeignKey("accounts.CustomUser",on_delete=models.PROTECT, null=True)
    active = models.BooleanField(default=True)

    paused = models.BooleanField(default=False)
    pause_start = models.DateTimeField(blank=True, null=True)
    pause_end = models.DateTimeField(blank=True, null=True)
    total_pause_duration = models.DurationField('Total Pause Duration', blank=True, default=datetime.timedelta(0))

    @property
    def total_hours_worked(self):
        if self.session_time and self.total_pause_duration:
            return self.session_time - self.total_pause_duration
        else:
            return self.session_time