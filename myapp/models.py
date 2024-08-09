from django.db import models

# Create your models here.
class Message(models.Model):
    DIRECTION_CHOICES = [
        ('incoming', 'Incoming'),
        ('outgoing', 'Outgoing'),
    ]

    from_number = models.CharField(max_length=15)
    to_number = models.CharField(max_length=15)
    body = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    direction = models.CharField(max_length=8, choices=DIRECTION_CHOICES)

    def __str__(self):
        return f"{self.direction} - {self.from_number} to {self.to_number}"
    

class ScannedPackageLog(models.Model):
    customer_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    tracking_number = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=[('Incoming', 'Incoming'), ('Outgoing', 'Outgoing')], default='Incoming')  # New field for status

    def __str__(self):
        return f"{self.customer_name} - {self.tracking_number}"

