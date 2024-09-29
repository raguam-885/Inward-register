from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import UploadedFile
from users.models import UserRole

@csrf_exempt
def upload_file(request):
    if request.method == 'POST':
        if 'file' not in request.FILES:
            return JsonResponse({"error": "No file provided"}, status=400)
        
        # Save the uploaded file
        to_list = request.POST.get('to')
        inward_from = request.POST.get('from')
        subject = request.POST.get('subject')
        content = request.POST.get('content')
        uploaded_file = UploadedFile(inward_from = inward_from, file=request.FILES['file'], subject=subject, content=content)
        uploaded_file.save()
        print(eval(to_list))
        uploaded_file.inward_to.add(*eval(to_list))

        return JsonResponse({"message": "File uploaded successfully", "file_id": uploaded_file.id}, status=201)

    return JsonResponse({"error": "Method not allowed"}, status=405)



@csrf_exempt
def inward_view(request):
    if request.method != 'GET':
        return JsonResponse({"error": "Method not allowed"}, status=405)
    
    user_id = request.GET.get('user_id')
    if not user_id:
        return JsonResponse({"error": "user_id is required"}, status=400)

    user = UserRole.objects.filter(user__id=user_id).first()
    if not user:
        return JsonResponse({"error": "User not found"}, status=404)

    inwards = {"message": "No inward messages for you."}

    if user.role in [UserRole.Departments, UserRole.Cell, UserRole.Committee] and user.department:
        inwards_queryset = UploadedFile.objects.filter(inward_to=user.department).prefetch_related('inward_to')
    else:
        inwards_queryset = UploadedFile.objects.all().prefetch_related('inward_to')

    # Convert the queryset to a list of dictionaries
    inwards_list = []
    for inward in inwards_queryset:
        inward_data = {
            "id": inward.id,
            "inward_from": inward.inward_from,
            "subject": inward.subject,
            "content": inward.content,
            "file": request.build_absolute_uri(inward.file.url) if inward.file else None,
            "created_on": inward.created_on.strftime('%B %d, %Y %I:%M %p'),  # Human-readable format
            "updated_on": inward.updated_on.strftime('%B %d, %Y %I:%M %p'),  # Human-readable format
            "inward_to": list(inward.inward_to.values('department_name', 'department_type'))  # Adjust 'id' and 'name' as per Department fields
        }
        inwards_list.append(inward_data)

    return JsonResponse(inwards_list, status=200, safe=False)

    