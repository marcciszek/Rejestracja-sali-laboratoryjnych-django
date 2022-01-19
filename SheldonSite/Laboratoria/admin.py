from django.contrib import admin
from .models import Room, RegistrationEntry, RegistrationPending


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'floor', 'room_number', 'room_station', 'status')
    list_filter = ('status', 'floor', 'room_number', 'room_station')
    search_fields = ('title', 'description', 'room_number', 'room_station')
    readonly_fields = ('slug',)

    def _check_permisson_room_admin(self, request):
        if request.user.is_superuser: return True
        if request.user.is_staff: return True
        return False

    def has_add_permission(self, request):
        return self._check_permisson_room_admin(request)

    def has_delete_permission(self, request, obj=None):
        return self._check_permisson_room_admin(request)

    def has_module_permission(self, request):
        return self._check_permisson_room_admin(request)

    def has_view_permission(self, request, obj=None):
        return self._check_permisson_room_admin(request)

    def has_change_permission(self, request, obj=None):
        return self._check_permisson_room_admin(request)


@admin.register(RegistrationEntry)
class RegistrationEntryAdmin(admin.ModelAdmin):
    # list_display = ('registerDate', 'roomConnector', 'reserved', 'pending')
    list_display = ('registerDate', 'roomConnector', 'reserved')
    readonly_fields = ('year_copy', 'month_copy',)

    def _check_permisson_entry_admin(self, request):
        if request.user.is_superuser: return True
        if request.user.is_staff: return True
        return False

    def has_add_permission(self, request):
        return self._check_permisson_entry_admin(request)

    def has_delete_permission(self, request, obj=None):
        return self._check_permisson_entry_admin(request)

    def has_module_permission(self, request):
        return self._check_permisson_entry_admin(request)

    def has_view_permission(self, request, obj=None):
        return self._check_permisson_entry_admin(request)

    def has_change_permission(self, request, obj=None):
        return self._check_permisson_entry_admin(request)

@admin.register(RegistrationPending)
class RegistrationPendingAdmin(admin.ModelAdmin):
    list_display = ('room',
                    'user',
                    'date',
                    'intervals',
                    'user_mentor',
                    'additional_info',
                    'processed')