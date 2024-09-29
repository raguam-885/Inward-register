from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Department(models.Model):
    SELF = "Self"
    AIDED = "Aided"
    Cell = "Cell"
    Committee = "Committee"
    TYPE_CHOICE = (
        (SELF, SELF),
        (AIDED, AIDED),
        (Cell, Cell),
        (Committee, Committee)
    )
    
    department_name = models.CharField(max_length=225, db_index=True)
    department_type = models.CharField(max_length=225, choices=TYPE_CHOICE, db_index=True)
    
    def __str__(self):
        return f"{self.department_type} - {self.department_name}"       
    class Meta:
        unique_together = ('department_name', 'department_type')
        
class UserRole(models.Model):
    Secretary = "Secretary"
    Principal = "Principal"
    Initiator = "Initiator"
    Office_Superintendent = "Office Superintendent"
    Departments = "Department"
    Cell = "Cell"
    Committee = "Committee"
    Admin = "Admin"
    ROLES_CHOICE = (
        (Secretary, Secretary), 
        (Principal, Principal),
        (Initiator, Initiator),
        (Office_Superintendent, Office_Superintendent),
        (Departments, Departments),
        (Admin, Admin),
        (Cell, Cell),
        (Committee, Committee),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)
    email = models.CharField(max_length=225, db_index=True)
    role = models.CharField(max_length=225, choices=ROLES_CHOICE, db_index=True)
    department = models.ForeignKey(Department, max_length=225, null=True, blank=True, db_index=True, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateField(auto_now=True)