from django.contrib import admin
from .models import Room


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'floor', 'room_number', 'room_station', 'status')
    list_filter = ('status', 'floor', 'room_number', 'room_station')
    search_fields = ('title', 'description', 'room_number', 'room_station')
    readonly_fields = ('slug',)

