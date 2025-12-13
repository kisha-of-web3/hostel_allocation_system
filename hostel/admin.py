from django.contrib import admin
from .models import Hostel, Room, Application, Allocation

@admin.register(Hostel)
class HostelAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'capacity', 'available_rooms')
    search_fields = ('name', 'location')


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('number', 'hostel', 'capacity', 'occupied', 'space_left', 'is_active')
    list_filter = ('hostel', 'is_active')
    search_fields = ('number', 'hostel__name')


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('student', 'preferred_hostel', 'preferred_room', 'status', 'created_at')
    list_filter = ('status', 'preferred_hostel')
    search_fields = ('student__username', 'preferred_hostel__name', 'preferred_room__number')


@admin.register(Allocation)
class AllocationAdmin(admin.ModelAdmin):
    list_display = ('student', 'room', 'allocated_at')
    search_fields = ('student__username', 'room__number')
    list_filter = ('room__hostel',)
