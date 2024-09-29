from django.contrib import admin
from users.models import UserRole, Department

# Register your models here.

class UserRolesAdmin(admin.ModelAdmin):
    list_display = ["email", "role", "department", "created_on", "updated_on"]
    
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ["id", "department_name", "department_type"]
    
admin.site.register(UserRole, UserRolesAdmin)
admin.site.register(Department, DepartmentAdmin)