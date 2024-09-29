from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from users.decorators import admin_required
from users.models import UserRole, Department
from django.views.decorators.csrf import csrf_exempt

from users.models import User, UserRole
# Create your views here.

@csrf_exempt
def admin_department_creation(request):
    if request.method != 'POST':
        return JsonResponse({"message": "Method not allowed"}, status=405)
    name = request.POST.get('department_name')
    depart_type = request.POST.get('department_type')
    
    if name and depart_type:
        try:
            if depart_type == Department.SELF:
                depart_type = Department.SELF
            elif depart_type == Department.AIDED:
                depart_type = Department.AIDED
            elif depart_type == Department.Cell:
                depart_type = Department.Cell
            elif depart_type == Department.Committee:
                depart_type = Department.Committee
            else:
                return JsonResponse({"message": "Department type match not found"}, status=404)
            department, create = Department.objects.get_or_create(department_name=name, department_type=depart_type)
            if create:
                return JsonResponse({"message": f"{name} - {depart_type} Department created successfully."}, status=200)
            else:
                return JsonResponse({"message": f"{name} - {depart_type} Department already exist."}, status=400)
        except Exception as e:
            return JsonResponse({"message": f"Error: {e}"})
    else:
        return JsonResponse({"message": "POST parameters missing"}, status=400)

@csrf_exempt
def department_list(request):
    if request.method != 'GET':
        return JsonResponse({"message": "Method not allowed"}, status=405)
    
    departments = [Department.SELF, Department.AIDED]
    department_dict = []
    
    for dept_type in departments:
        data = list(Department.objects.filter(department_type=dept_type).values('department_name', 'department_type'))
        for dept in data:
            department_dict.append({"name": dept['department_name'], "type": dept['department_type']})
    
    return JsonResponse(department_dict, status=200, safe=False)

@csrf_exempt
def cell_list(request):
    if request.method != 'GET':
        return JsonResponse({"message": "Method not allowed"}, status=405)
    
    department_dict = []
    data = list(Department.objects.filter(department_type=Department.Cell).values('department_name', 'department_type'))
    for dept in data:
        department_dict.append({"name": dept['department_name']})
    
    return JsonResponse(department_dict, status=200, safe=False)

@csrf_exempt
def committee_list(request):
    if request.method != 'GET':
        return JsonResponse({"message": "Method not allowed"}, status=405)
    
    department_dict = []
    data = list(Department.objects.filter(department_type=Department.Committee).values('department_name', 'department_type'))
    for dept in data:
        department_dict.append({"name": dept['department_name']})
    
    return JsonResponse(department_dict, status=200, safe=False)

@csrf_exempt
def user_list(request):
    if request.method != 'GET':
        return JsonResponse({"message": "Method not allowed"}, status=405)
    users = UserRole.objects.all().values('user__id', 'user__username', 'user__email', 'role', 'department__department_name', 'department__department_type')
    user_data = [
        {
            "id": user["user__id"],
            "name": user["user__username"],
            "email": user["user__email"],
            "role": user['role'],
            "department_name": user["department__department_name"],
            "department_type": user["department__department_type"]
        }
        for user in users
    ]
    return JsonResponse(user_data, status=200, safe=False)


@csrf_exempt
def user_creation_choice_field(request):
    if request.method != 'GET':
        return JsonResponse({"message": "Method not allowed"}, status=405)
    type_of = request.GET.get('type')
    department_dict = []
    
    if 'department' in type_of.lower():
        departments = [Department.SELF, Department.AIDED]
        data = list(Department.objects.filter(department_type__in=departments).values('department_name', 'department_type'))
        for dept in data:
            department_dict.append({"name": dept['department_name'], "type": dept['department_type']})
    if 'cell' in type_of.lower():
        data = list(Department.objects.filter(department_type=Department.Cell).values('department_name', 'department_type'))
        for dept in data:
            department_dict.append({"name": dept['department_name'], "type": dept['department_type']})
    if 'committee' in type_of.lower():
        data = list(Department.objects.filter(department_type=Department.Committee).values('department_name', 'department_type'))
        for dept in data:
            department_dict.append({"name": dept['department_name'], "type": dept['department_type']})
    return JsonResponse(department_dict, safe=False, status=200)
    


@csrf_exempt
def choice_field(request):
    if request.method != 'GET':
        return JsonResponse({"message": "Method not allowed"}, status=405)
    
    type_of = request.GET.get('type')
    department_dict = []
    
    if 'department' in type_of.lower():
        self_departments = list(Department.objects.filter(department_type=Department.SELF).values('department_name', 'id'))
        aided_departments = list(Department.objects.filter(department_type=Department.AIDED).values('department_name', 'id'))
        department_dict.extend([{"value": dept['id'], "label": dept['department_name']} for dept in self_departments])
        department_dict.extend([{"value": dept['id'], "label": dept['department_name']} for dept in aided_departments])
        
    if 'cell' in type_of.lower():
        cell_departments = list(Department.objects.filter(department_type=Department.Cell).values('department_name', 'id'))
        department_dict.extend([{"value": dept['id'], "label": dept['department_name']} for dept in cell_departments])
        
    if 'committee' in type_of.lower():
        committee_departments = list(Department.objects.filter(department_type=Department.Committee).values('department_name', 'id'))
        department_dict.extend([{"value": dept['id'], "label": dept['department_name']} for dept in committee_departments])
        
    return JsonResponse(department_dict, safe=False, status=200)


@csrf_exempt
@admin_required
def user_creation(request):
    if request.method != 'POST':
        return JsonResponse({"message": "Method not allowed"}, status=405)
    
    email = request.POST.get('email')
    role = request.POST.get('role')
    password = request.POST.get('password')
    department_type = request.POST.get('department_type')
    department = request.POST.get('department')
    name = request.POST.get('user_name')
    # Validate the input
    if not email or not role or not password or not name:
        return JsonResponse({"message": "Missing required fields"}, status=400)
    
    # Check if the role is valid
    if role not in dict(UserRole.ROLES_CHOICE).keys():
        return JsonResponse({"message": "Invalid role"}, status=400)
    
    # Create the user
    try:
        if role.lower() == "admin":
            user = User.objects.create_superuser(username=email, email=email, password=password, first_name=name)
        else:
            user = User.objects.create_user(username=email, email=email, password=password, first_name=name)
    except Exception as e:
        return JsonResponse({"message": f"Error creating user: {str(e)}"}, status=400)
    
    # Create the user role
    try:
        if role in ['Department', 'Cell', 'Committee']:
            department_obj = Department.objects.filter(department_type=department_type, department_name=department)
            if department_obj.exists():
                department_obj = department_obj.first()
                user_role = UserRole.objects.create(user=user, email=email, role=role, department=department_obj)
            else:
                return JsonResponse({"message": "Department details is missing"}, status=400)
        else:
            user_role = UserRole.objects.create(user=user, email=email, role=role)
    except Exception as e:
        # If creating user role fails, delete the created user
        user.delete()
        return JsonResponse({"message": f"Error creating user role: {str(e)}"}, status=400)
    
    return JsonResponse({"message": "User and role created successfully"}, status=201)
