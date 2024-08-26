from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User,Document,ExtractedText,AIText
# Register your models here.

class CustomUserAdmin(UserAdmin):
    # The fields to be used in displaying the User model.
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active', 'is_superuser')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser','is_verified')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2', 'is_staff', 'is_active', 'is_verified'),
        }),
    )

    readonly_fields = ('date_joined', 'last_login')


admin.site.register(User)
admin.site.register(Document)
admin.site.register(ExtractedText)
admin.site.register(AIText)