from django.contrib.auth.backends import ModelBackend
from .models import CustomUser

class PhoneNumberAuthBackend(ModelBackend):
    """Authenticate using phone number instead of username or email."""
    def authenticate(self, request, phone_number=None, password=None, **kwargs):
        try:
            user = CustomUser.objects.get(phone_number=phone_number)
            if user.check_password(password):
                return user
        except CustomUser.DoesNotExist:
            return None
