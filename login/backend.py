from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User


def back_authenticate(email, password):
    try:
        user = User.objects.get(email=email)
    except Exception as e:
        return None
    user = authenticate(username=email, password=password)
    return user


def back_login(request, user):
    login(request, user)
    # request.session['user'] = user.id
