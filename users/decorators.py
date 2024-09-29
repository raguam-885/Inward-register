from django.http import HttpResponseForbidden, JsonResponse
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

def admin_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return JsonResponse({"message":"Token not provided or invalid."}, status=403)

        token_key = auth_header.split(' ')[1]
        try:
            token = Token.objects.get(key=token_key)
            user = token.user
        except Token.DoesNotExist:
            return JsonResponse({"message":"Invalid token."}, status=403)

        if not user.is_staff and not user.is_superuser:
            return JsonResponse({"message":"You are not authorized to access this page."} , status=403)

        return view_func(request, *args, **kwargs)
    return _wrapped_view
