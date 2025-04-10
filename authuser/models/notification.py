from django.db import models
from authuser.models import User
from uuid import uuid4


class Modification(models.Model):
    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True)  
    
    class Meta:
        abstract = True 

class CallNotification(Modification):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender_notifications')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_notifications')
    read = models.BooleanField(default=False)

    class Meta:
            db_table = "notification_table"
            
    def __str__(self):
        return f'{self.sender.first_name} to {self.receiver.last_name}'
    

