from django.contrib import admin
from users.models import CustomUser

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'date_joined', 'last_login', 'is_active', 'is_staff', 'is_superuser']
    list_filter = ['is_staff', 'is_superuser', 'is_active']
    search_fields = ['username', 'email', 'date_joined']
    
    class Meta:
        model = CustomUser
        

admin.site.register(CustomUser, CustomUserAdmin)