from rest_framework.views import exception_handler
from rest_framework.exceptions import PermissionDenied
from backend.models.Offence import Offence

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if isinstance(exc, PermissionDenied):
        offence = {
            "user": str(context["request"].user.pk),
            "description": f'User tried to access {context["request"].path}'
        }
        Offence.objects.create(user = context["request"].user, description = f'User tried to access {context["request"].path}')


    return response