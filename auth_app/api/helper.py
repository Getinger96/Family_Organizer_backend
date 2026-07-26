
import json
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from email.mime.image import MIMEImage

from django.contrib.staticfiles import finders
from functools import lru_cache

childs = []

def get_child_data(children_data):
    new_child_list = []
    for i, child in enumerate(children_data):
        new_child_list.append({
        "id": i,
           "name": child["name"],
        "age": child["age"]
        })
        
    return new_child_list

    
    
def sendingEmail(contex, email_to):
    message = EmailMultiAlternatives(
        subject="Register",
        body=contex,
        from_email=settings.EMAIL_HOST_USER,
        to=[email_to],
    )
    
    message.attach_alternative(contex, "text/html")
    message.attach(logo_data())
    try:
        message.send()
        return True
    except Exception as e:
        print("EMAIL FEHLER:", e)
        return False
    
    
@lru_cache()
def logo_data():
    with open(finders.find('logo/icon_home.png'), 'rb') as f:
        logo_data = f.read()
    logo = MIMEImage(logo_data, _subtype="png")
    logo.add_header('Content-ID', '<logo>')
    return logo