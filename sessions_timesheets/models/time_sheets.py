from django.db import models

class TimeSheet(models.Model):
    name = models.CharField(max_length=200,null=True)
    week_of = models.DateField('Week Of',null=True)