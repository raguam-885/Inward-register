from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from users.models import UserRole  # Make sure to adjust this import based on your actual models
import json

@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        try:
            # data = json.loads(request.body)
            email = request.POST.get('email')
            password = request.POST.get('password')
            email = email.strip() if email else None

            user = authenticate(request, username=email, password=password)
            if user is not None:
                token, created = Token.objects.get_or_create(user=user)
                user_details = UserRole.objects.filter(user=user).values(
                    'user__id', 'user__email', 'role', 'department__department_name', 'department__department_type', 'user__first_name'
                ).first()
                if user_details:
                    data = {
                        "user_id": user_details.get('user__id'),
                        "user_name": user_details.get('user__first_name'),
                        "email": user_details.get('user__email'),
                        "role": user_details.get('role'),
                        "department_type": user_details.get('department__department_type'),
                        "department_name": user_details.get('department__department_name'),
                        "token": token.key
                    }
                    return JsonResponse({'message': 'Login successful', 'data': data}, status=200)
                else:
                    return JsonResponse({'message': 'User role details not found'}, status=404)
            else:
                return JsonResponse({'message': 'Invalid credentials'}, status=401)
        except json.JSONDecodeError:
            return JsonResponse({'message': 'Invalid JSON'}, status=400)
    return JsonResponse({'message': 'Only POST method is allowed'}, status=405)
