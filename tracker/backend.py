from django.contrib.auth.backends import ModelBackend
from .models import CustomUser

class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = CustomUser.objects.get(email=username)
            
            if user.check_password(password) and user.is_active:
                return user
            return None
        except CustomUser.DoesNotExist:
            return None  
