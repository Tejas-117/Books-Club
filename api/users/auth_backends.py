from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

class EmailBackend(ModelBackend):
    """
        Custom Backend to authenticate user based on email and password fields.
    """
    def authenticate(self, request, **kwargs):
        UserModel = get_user_model()

        try:
            # check if the email field is empty.
            email = kwargs.get('email', None)
            if email is None:
                return None

            # check if the password field matches with the password saved in database.
            user = UserModel.objects.get(email__exact=email)
            if user.check_password(kwargs.get('password', None)):
                return user
        except UserModel.DoesNotExist:
            return None
            
        return None