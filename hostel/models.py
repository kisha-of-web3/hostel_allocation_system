from django.db import models
from django.conf import settings 

# Create your models here.

class Hostel(models.Model):
    name = models.CharField(max_length=120)
    location = models.CharField(max_length=255, blank=True)
    capacity = models.PositiveIntegerField() # total capacity
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
    
    @property
    def available_rooms(self):
     #count allocated applications
     from .models import Application
     booked = Application.objects.filter(preferred_hostel=self, status='approved').count()
     return self.capacity - booked
     

class Room(models.Model):
    hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE, related_name='rooms')
    number = models.CharField(max_length=30)
    capacity = models.PositiveIntegerField(default=1)
    occupied = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('hostel', 'number')

    def __str__(self):
        return f"{self.hostel.name} - {self.number}"
    @property
    def space_left(self):
        return max(self.capacity - self.occupied, 0)

class Application(models.Model):
    PENDING = 'pending'
    APPROVED = 'approved'
    REJECTED = 'rejected'
    STATUS_CHOICES = ((PENDING,'Pending'), (APPROVED,'Approved'), (REJECTED,'Rejected'))

    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='applications')
    preferred_hostel = models.ForeignKey(Hostel, null=True, blank=True, on_delete=models.SET_NULL)
    preferred_room = models.ForeignKey(Room, null=True, blank=True, on_delete=models.SET_NULL)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    note = models.TextField(blank=True)

    def __str__(self):
        return f"{self.student.username} - {self.status}"

class Allocation(models.Model):
    student = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='allocation')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='applications')
    allocated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.username} -> {self.room}"
