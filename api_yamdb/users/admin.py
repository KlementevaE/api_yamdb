from django.contrib import admin

from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'username', 'email', 'role', 'bio',
                    'first_name', 'last_name', 'confirmation_code')
    fields = ('username', 'email', 'role', 'bio',
              'first_name', 'last_name', 'confirmation_code', "is_staff")


admin.site.register(User, UserAdmin)
