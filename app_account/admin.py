from django.contrib import admin
from .models import User



class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'is_author', 'is_vip_due_date']
    # list_filter = ['']
    # search_fields = [']
    # raw_id_fields = ['']
    # date_hierarchy = ''
    # ordering = ['']

admin.site.register(User, UserAdmin)