from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin

from django.utils.translation import gettext, gettext_lazy as _

from .models import Profile


class UserProfileInLine(admin.TabularInline):
    model = Profile
    can_delete = False
    fk_name = 'user'


class CustomUserAdmin(UserAdmin):
    inlines = [UserProfileInLine]

    list_filter = ('is_staff', 'is_superuser', 'is_active', 'profile__user_rank')
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_user_rank_name')
    list_select_related = ('profile',)

    readonly_fields = [
        "first_name",
        "last_name",
        "email",
        "username",
        "last_login",
        "date_joined",
        'is_superuser'
    ]
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined',)}),
    )

    def get_user_rank_name(self, instance):
        return instance.profile.Rank(instance.profile.user_rank).name
    get_user_rank_name.short_description = 'Rank_name'

    def user_rank(self, obj):
        return obj.profile.user_rank
    user_rank.short_description = 'user_rank'

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.unregister(User)
admin.site.unregister(Group)
admin.site.register(User, CustomUserAdmin)
