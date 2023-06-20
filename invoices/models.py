from django.db import models

# Create your models here.
class Invoice(models.Model):
    task = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
    date_completed = models.DateTimeField(auto_now_add=True)
    total_hours = models.DecimalField(max_digits=3, decimal_places=1)

    def __str__(self):
        return self.task