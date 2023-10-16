# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from .forms import LoginForm, SignUpForm
from .models import User
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.hashers import make_password
from apps.home.models import Department
from django.contrib.auth.decorators import login_required


def login_view(request):
    form = LoginForm(request.POST or None)

    msg = None

    if request.method == "POST":

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/dep_management/')
            else:
                msg = 'Invalid credentials'
        else:
            msg = 'Error validating the form'

    return render(request, "accounts/login.html", {"form": form, "msg": msg})


def register_user(request):
    msg = None
    success = False

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()

            department = form.cleaned_data['department']
            user.set_department = department
            user.is_superuser = form.cleaned_data.get('is_admin')

            user.save()

            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)

            login(request, user)

            msg = 'User created successfully.'
            success = True

            return redirect("/login/")
        else:
            msg = 'Form is not valid'
    else:
        form = SignUpForm()

    return render(request, "accounts/register.html", {"form": form, "msg": msg, "success": success})



@login_required
def modify_user(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        updated_username = request.POST.get('username')
        updated_email = request.POST.get('email')
        updated_department_id = request.POST.get('department_id')
        updated_role = request.POST.get('is_superuser') == 'true'  # Convert string to boolean

        department = get_object_or_404(Department, id=updated_department_id)
        # Update the user's information in the database
        user.username = updated_username
        user.email = updated_email
        user.department = department
        user.is_superuser = updated_role
        user.save()

        # Return the updated department name and role as a JSON response
        department_name = user.department.name if user.department else ""
        role = "Admin" if user.is_superuser else "User"
        return JsonResponse({'department_name': department_name, 'role': role})

    # If the request method is not POST, return a JsonResponse with an error message
    return JsonResponse({'error': 'Invalid request method'}, status=400)

@login_required
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        user.delete()
    return redirect('users')

def user_management(request):
    user_list = User.objects.all()
    department_list = Department.objects.all()

    context = {
        'user_list': user_list,
        'department_list': department_list,
    }
    return render(request, 'accounts/users.html', context)
