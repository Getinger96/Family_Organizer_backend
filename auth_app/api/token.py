from django.contrib.auth.tokens import PasswordResetTokenGenerator
import os, random, string
from auth_app.models import Child 
class generate_token(PasswordResetTokenGenerator):
    
    
    
 def _make_hash_value(self, user, timestamp):
     
     return f"{user.pk}{timestamp}{user.is_active}"
 
account_activation_token = generate_token()


def generate_token_for_childs(user, child_data):
    pass



def generate_random_token():
    length = 6
    chars = string.ascii_letters + string.digits + '!@#$%^&*()'

    token =  ''.join(random.choice(chars) for i in range(length))
    
    if not Child.objects.filter(password=token).exists():
        return token