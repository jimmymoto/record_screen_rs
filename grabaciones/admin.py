from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from grabaciones.models import License, UserProfile, UserGroups, Session, Grabaciones
# Register your models here.
admin.site.unregister(User)


class LicenseAdmin(admin.ModelAdmin):
    model = License
    list_display = ['id', 'clientId', 'stateLicense']


class UserGroupsAdmin(admin.ModelAdmin):
    pass


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    filter_horizontal = ('user_groups',)


class CustomUserAdmin(UserAdmin):
    save_on_top = True
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'last_login')
    inlines = [UserProfileInline]


class SessionAdmin(admin.ModelAdmin):
    model = Session
    list_display = ['sessionId', 'agente', 'createdAt']


class GrabacionesAdmin(admin.ModelAdmin):
    model = Grabaciones
    list_display = ['grabacionesId', 'size', 'duration', 'url', 'status', 'createdAt']


admin.site.register(License, LicenseAdmin)
admin.site.register(User, CustomUserAdmin)
admin.site.register(UserGroups, UserGroupsAdmin)
admin.site.register(Session, SessionAdmin)
admin.site.register(Grabaciones, GrabacionesAdmin)
