from django.contrib.auth.backends import ModelBackend,BaseBackend
from django.contrib.auth import get_user_model
from .models import CustomUser
from django.contrib.auth.models import User

class EmailBackend(ModelBackend):
    def authenticate(self,username=None,password=None, **kwargs):
        Usermodel=get_user_model()
        print(Usermodel)
        try:
            user=Usermodel.objects.get(email=username)
            print("inside backend email : ",user)
        except Usermodel.DoesNotExist:
            return None
        else:
            print(user.password)
            print(user.check_password(password))
            if user.check_password(password):
                return user
            
        return None