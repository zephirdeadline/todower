# -*- coding: utf-8 -*-
from django.shortcuts import render
from .backend import back_authenticate, back_login
from login.forms import *
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth import logout
from .models import Member


def index(request):
    if request.method == "POST":
        if 'login_submit' in request.POST:
            form_signin = UserForm(request.POST)
            if form_signin.is_valid():
                email = form_signin.cleaned_data["email"]
                password = form_signin.cleaned_data["password"]
                user = back_authenticate(email=email, password=password)
                if user:
                    back_login(request, user)
                    return HttpResponseRedirect('/main/')
                else:
                    messages.add_message(request, messages.ERROR, 'Une erreur critique est survenue.', extra_tags="danger")
        if 'register_submit' in request.POST:
            form_user = UserForm(request.POST)
            if form_user.is_valid():
                user = form_user.save(commit=False)
                user.username = user.email
                user.set_password(user.password)
                user.save()
                member = Member()
                member.user = user
                member.save()
                back_login(request, user)
                messages.success(request, 'User create with success')
                return HttpResponseRedirect('/main/')
            else:
                messages.add_message(request, messages.ERROR, 'Bad formulaire', extra_tags='danger')
    form_user = UserForm()
    return render(request, 'login/index.html', locals())


def logout_render(request):
    messages.success(request, 'Déconnexion réussie')
    logout(request)
    return render(request, 'login/logout.html')


