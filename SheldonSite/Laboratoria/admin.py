from django.contrib import admin
from .models import Room


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'floor', 'room_number', 'status')
    list_filter = ('status', 'floor', 'room_number')
    search_fields = ('title', 'description', 'room_number')
    readonly_fields = ('slug',)

