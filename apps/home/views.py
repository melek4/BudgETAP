# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template import loader
from django.urls import reverse
from .forms import DepartmentForm, SubDepartmentForm, CategoryForm, SubCategoryForm, SubSubCategoryForm, BudgetAllocationForm
from .models import Department, SubDepartment, Category, SubCategory, SubSubCategory, BudgetAllocation
from django.shortcuts import render, redirect, get_object_or_404
import json
from django.views.generic import ListView
from django.db.models import Sum

@login_required(login_url="/login/")
def index(request):
    
    return redirect('dep_management')  


@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:dep_management'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def create_department(request):
    if request.method == "POST":
        form = DepartmentForm(request.POST)
        if form.is_valid():
            #form.save()
            name = form.cleaned_data['name']
            department = Department(name=name)
            department.save()
            #return redirect('liste_departements')  # Redirige vers une page de liste de départements
            # Get the subdepartment ID
            department_id = department.id

            # Prepare the response data
            response_data = {
                'department_id': department_id,
            }

            # Convert the response data to JSON
            response_json = json.dumps(response_data)

            # Return a success response
            return HttpResponse(response_json, content_type='application/json')
    else:
        return JsonResponse({'error': 'Invalid request method.'})

@login_required(login_url="/login/")
def modify_department(request, department_id):
    department = get_object_or_404(Department, id=department_id)
    if request.method == 'POST':
        form = DepartmentForm(request.POST, instance=department)
        if form.is_valid():
            form.save()
            return redirect('dep_management')  # Redirect to 'departments' URL by name
    else:
        form = DepartmentForm(instance=department)
    return render(request, 'home/management/departments.html', {'form': form, 'department': department, 'department_id': department_id, 'department_name':department.name})

@login_required(login_url="/login/")
def delete_department(request, department_id):
    department = get_object_or_404(Department, id=department_id)
    if request.method == 'POST':
        department.delete()
        return HttpResponse()
    return HttpResponse(status=204)

@login_required(login_url="/login/")
def dep_management(request):
    context = {}
    if(request.user.is_superuser):
        dep_list = Department.objects.all().order_by('name')
    else:
        dep_list = Department.objects.filter(id=request.user.department.id)
    # add the dictionary during initialization
    context["dep_list"] = dep_list

    return render(request, "home/management/departments.html", context)



@login_required(login_url="/login/")
def create_subdepartment(request, department_id):
    if request.method == "POST":
        department_id = request.POST.get("department_id")
        subdepartment_name = request.POST.get("subdepartment_name")

        # Perform the necessary validation and error handling

        # Save the subdepartment to the database
        department = Department.objects.get(id=department_id)
        subdepartment = SubDepartment(department=department, name=subdepartment_name)
        subdepartment.save()
        # Get the subdepartment ID
        subdepartment_id = subdepartment.id

        # Prepare the response data
        response_data = {
            'subdepartment_id': subdepartment_id,
        }

        # Convert the response data to JSON
        response_json = json.dumps(response_data)

        # Return a success response
        return HttpResponse(response_json, content_type='application/json')
    else:
        return JsonResponse({'error': 'Invalid request method.'})
    
@login_required(login_url="/login/")
def subdep_management(request, department_id):
    context = {}
    department = get_object_or_404(Department, id=department_id)
    subdepartments = department.sub_departments.all()
    # add the dictionary during initialization
    context = {
        'department': department,
        'subdepartments': subdepartments,
    }

    return render(request, "home/management/subdepartments.html", context)

@login_required(login_url="/login/")
def modify_subdepartment(request, department_id, subdepartment_id):
    subdepartment = get_object_or_404(SubDepartment, id=subdepartment_id)
    if request.method == 'POST':
        form = SubDepartmentForm(request.POST, instance=subdepartment)
        if form.is_valid():
            form.save()
    else:
        form = SubDepartmentForm(instance=subdepartment)
    return render(request, 'home/management/subdepartments.html', {'form': form, 'subdepartment': subdepartment, 'subdepartment_id': subdepartment_id})

@login_required(login_url="/login/")
def delete_subdepartment(request, department_id, subdepartment_id):
    subdepartment = get_object_or_404(SubDepartment, id=request.POST.get('subdepartment_id'))
    if request.method == 'POST':
        subdepartment.delete()
        return HttpResponse()
    return HttpResponse(status=204)



@login_required(login_url="/login/")
def create_category(request, subdepartment_id):
    if request.method == "POST":
        category_name = request.POST.get("category_name")

        # Perform the necessary validation and error handling

        # Save the subdepartment to the database
        subdepartment = SubDepartment.objects.get(id=subdepartment_id)
        category = Category(subdepartment=subdepartment, name=category_name)
        category.save()
        # Get the subdepartment ID
        category_id = category.id

        # Prepare the response data
        response_data = {
            'category_id': category_id,
        }

        # Convert the response data to JSON
        response_json = json.dumps(response_data)

        # Return a success response
        return HttpResponse(response_json, content_type='application/json')
    else:
        return JsonResponse({'error': 'Invalid request method.'})

@login_required(login_url="/login/")
def modify_category(request, subdepartment_id, category_id):
    category = get_object_or_404(Category, id=category_id)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
    else:
        form = CategoryForm(instance=category)
    return render(request, 'home/management/categories.html', {'form': form, 'category': category, 'category_id': category_id})

@login_required(login_url="/login/")
def delete_category(request, subdepartment_id, category_id):
    category = get_object_or_404(Category, id=category_id)
    if request.method == 'POST':
        category.delete()
        return HttpResponse()
    return HttpResponse(status=204)

@login_required(login_url="/login/")
def cat_management(request, subdepartment_id=1):
    subdepartment = get_object_or_404(SubDepartment, id=subdepartment_id)
    department = subdepartment.department
    categories = subdepartment.categories.all()

    context = {
        'department': department,
        'subdepartment': subdepartment,
        'categories': categories,
    }

    return render(request, 'home/management/categories.html', context)



@login_required(login_url="/login/")
def create_subcategory(request, category_id):
    if request.method == "POST":
        subcategory_name = request.POST.get("subcategory_name")

        # Perform the necessary validation and error handling

        # Save the subdepartment to the database
        category = Category.objects.get(id=category_id)
        subcategory = SubCategory(category=category, name=subcategory_name)
        subcategory.save()
        # Get the subdepartment ID
        subcategory_id = subcategory.id

        # Prepare the response data
        response_data = {
            'subcategory_id': subcategory_id,
        }

        # Convert the response data to JSON
        response_json = json.dumps(response_data)

        # Return a success response
        return HttpResponse(response_json, content_type='application/json')
    else:
        return JsonResponse({'error': 'Invalid request method.'})

@login_required(login_url="/login/")
def modify_subcategory(request, category_id, subcategory_id):
    subcategory = get_object_or_404(SubCategory, id=subcategory_id)
    if request.method == 'POST':
        form = SubCategoryForm(request.POST, instance=subcategory)
        if form.is_valid():
            form.save()
    else:
        form = SubCategoryForm(instance=subcategory)
    return render(request, 'home/management/subcategories.html', {'form': form, 'subcategory': subcategory, 'subcategory_id': subcategory_id})

@login_required(login_url="/login/")
def delete_subcategory(request, category_id, subcategory_id):
    subcategory = get_object_or_404(SubCategory, id=subcategory_id)
    if request.method == 'POST':
        subcategory.delete()
        return HttpResponse()
    return HttpResponse(status=204)

@login_required(login_url="/login/")
def subcat_management(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    subdepartment = category.subdepartment
    department = subdepartment.department
    subcategories = category.sub_categories.all()

    context = {
        'department': department,
        'subdepartment': subdepartment,
        'category': category,
        'subcategories': subcategories,
    }

    return render(request, 'home/management/subcategories.html', context)




@login_required(login_url="/login/")
def create_subsubcategory(request, subcategory_id):
    if request.method == "POST":
        subsubcategory_name = request.POST.get("subsubcategory_name")

        # Perform the necessary validation and error handling

        # Save the subsubcategory to the database
        subcategory = SubCategory.objects.get(id=subcategory_id)
        subsubcategory = SubSubCategory(subcategory=subcategory, name=subsubcategory_name)
        subsubcategory.save()
        # Get the subsubcategory ID
        subsubcategory_id = subsubcategory.id

        # Prepare the response data
        response_data = {
            'subsubcategory_id': subsubcategory_id,
        }

        # Convert the response data to JSON
        response_json = json.dumps(response_data)

        # Return a success response
        return HttpResponse(response_json, content_type='application/json')
    else:
        return JsonResponse({'error': 'Invalid request method.'})

@login_required(login_url="/login/")
def modify_subsubcategory(request, subcategory_id, subsubcategory_id):
    subsubcategory = get_object_or_404(SubSubCategory, id=subsubcategory_id)
    if request.method == 'POST':
        form = SubSubCategoryForm(request.POST, instance=subsubcategory)
        if form.is_valid():
            form.save()
    else:
        form = SubSubCategoryForm(instance=subsubcategory)
    return render(request, 'home/management/subsubcategories.html', {'form': form, 'subsubcategory': subsubcategory, 'subsubcategory_id': subsubcategory_id})

@login_required(login_url="/login/")
def delete_subsubcategory(request, subcategory_id, subsubcategory_id):
    subsubcategory = get_object_or_404(SubSubCategory, id=subsubcategory_id)
    if request.method == 'POST':
        subsubcategory.delete()
        return HttpResponse()
    return HttpResponse(status=204)

@login_required(login_url="/login/")
def subsubcat_management(request, subcategory_id):
    subcategory = get_object_or_404(SubCategory, id=subcategory_id)
    category = subcategory.category
    subdepartment = category.subdepartment
    department = subdepartment.department
    subsubcategories = subcategory.sub_subcategories.all()

    context = {
        'department': department,
        'subdepartment': subdepartment,
        'category': category,
        'subcategory': subcategory,
        'subsubcategories': subsubcategories,
    }

    return render(request, 'home/management/subsubcategories.html', context)

@login_required(login_url="/login/")
def dep_budget_set(department_id, year):
    department = get_object_or_404(Department, id=department_id)
    subdepartments = department.sub_departments.all()

    total_budget = 0
    for subdep in subdepartments:
        subdep_budgets = BudgetAllocation.objects.filter(subdepartment=subdep, year=year)
        subdep_budget_sum = subdep_budgets.aggregate(total_budget=Sum('budget'))['total_budget']
        total_budget += subdep_budget_sum if subdep_budget_sum else 0

    BudgetAllocation.objects.filter(department=department, year=year).update(budget=total_budget)

@login_required(login_url="/login/")
def subdep_budget_set(subdepartment_id,year):
    subdepartment = get_object_or_404(SubDepartment, id=subdepartment_id)
    categories = subdepartment.categories.all()
    total_budget = 0
    for cat in categories:
        cat_budgets = BudgetAllocation.objects.filter(category=cat, year=year)
        cat_budget_sum = cat_budgets.aggregate(total_budget=Sum('budget'))['total_budget']
        total_budget += cat_budget_sum if cat_budget_sum else 0

    BudgetAllocation.objects.filter(subdepartment=subdepartment, year=year).update(budget=total_budget)

@login_required(login_url="/login/")
def cat_budget_set(category_id,year):
    category = get_object_or_404(Category, id=category_id)
    subcategories = category.sub_categories.all()
    total_budget = 0
    for subcat in subcategories:
        subcat_budgets = BudgetAllocation.objects.filter(subcategory=subcat, year=year)
        subcat_budget_sum = subcat_budgets.aggregate(total_budget=Sum('budget'))['total_budget']
        total_budget += subcat_budget_sum if subcat_budget_sum else 0

    BudgetAllocation.objects.filter(category=category, year=year).update(budget=total_budget)

@login_required(login_url="/login/")
def subcat_budget_set(subcategory_id,year):
    subcategory = get_object_or_404(SubCategory, id=subcategory_id)
    subsubcategories = subcategory.sub_subcategories.all()
    total_budget = 0
    for subsubcat in subsubcategories:
        subsubcat_budgets = BudgetAllocation.objects.filter(subsubcategory=subsubcat, year=year)
        subsubcat_budget_sum = subsubcat_budgets.aggregate(total_budget=Sum('budget'))['total_budget']
        total_budget += subsubcat_budget_sum if subsubcat_budget_sum else 0

    BudgetAllocation.objects.filter(subcategory=subcategory, year=year).update(budget=total_budget)
    

@login_required(login_url="/login/")
def dep_budget_allocation(request):
    if request.method == 'POST':
        year = request.POST.get('year')  # Get the value of the year field
        if request.user.is_superuser:
            departments = Department.objects.all().order_by('name')
        else :
            departments = Department.objects.filter(id=request.user.department.id)
        

        for department in departments:
            budget_field_name = f"budget-{department.id}"
            description_field_name = f"description-{department.id}"

            budget = request.POST.get(budget_field_name)
            description = request.POST.get(description_field_name)

            if budget:
                # Save the budget and description for the department along with the year
                allocation = BudgetAllocation.objects.create(
                    department=department,
                    budget=budget,
                    description=description,
                    year=year
                )
                allocation.save()

        # Redirect to a success page or perform any other action after saving the data
        return redirect('dep_budget_allocation')

    else:
        if request.user.is_superuser:
            departments = Department.objects.all().order_by('name')
        else :
            departments = Department.objects.filter(id=request.user.department.id)

    context = {
        'departments': departments,
    }

    return render(request, 'home/budget allocation/departments.html', context)



@login_required(login_url="/login/")
def subdep_budget_allocation(request, department_id):
    department = get_object_or_404(Department, id=department_id)
    subdepartments = SubDepartment.objects.filter(department=department)

    if request.method == 'POST':
        year = request.POST.get('year')  # Get the value of the year field
        for subdepartment in subdepartments:
            budget_field_name = f"budget-{subdepartment.id}"
            description_field_name = f"description-{subdepartment.id}"

            budget = request.POST.get(budget_field_name)
            description = request.POST.get(description_field_name)

            if budget:
                # Save the budget and description for the subdepartment along with the year
                allocation = BudgetAllocation.objects.create(
                    subdepartment=subdepartment,
                    budget=budget,
                    description=description,
                    year=year
                )
                allocation.save()
        dep_budget_set(department_id, year)
        # Redirect to a success page or perform any other action after saving the data
        return redirect('subdep_budget_allocation', department_id=department_id)

    context = {
        'department': department,
        'subdepartments': subdepartments,
    }

    return render(request, 'home/budget allocation/subdepartments.html', context)

@login_required(login_url="/login/")
def cat_budget_allocation(request, subdepartment_id):
    subdepartment = get_object_or_404(SubDepartment, id=subdepartment_id)
    dep_id = subdepartment.department.id
    categories = Category.objects.filter(subdepartment=subdepartment)

    if request.method == 'POST':
        year = request.POST.get('year')  # Get the value of the year field
        for category in categories:
            budget_field_name = f"budget-{category.id}"
            description_field_name = f"description-{category.id}"

            budget = request.POST.get(budget_field_name)
            description = request.POST.get(description_field_name)

            if budget:
                # Save the budget and description for the subdepartment along with the year
                allocation = BudgetAllocation.objects.create(
                    category=category,
                    budget=budget,
                    description=description,
                    year=year
                )
                allocation.save()
        subdep_budget_set(subdepartment_id, year)
        dep_budget_set(dep_id, year)
        # Redirect to a success page or perform any other action after saving the data
        return redirect('cat_budget_allocation', subdepartment_id=subdepartment_id)

    context = {
        'dep_id': dep_id,
        'subdepartment': subdepartment,
        'categories': categories,
    }

    return render(request, 'home/budget allocation/categories.html', context)


@login_required(login_url="/login/")
def subcat_budget_allocation(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    subdep_id = category.subdepartment.id
    dep_id = category.subdepartment.department.id
    subcategories = SubCategory.objects.filter(category=category)

    if request.method == 'POST':
        year = request.POST.get('year')  # Get the value of the year field
        for subcategory in subcategories:
            budget_field_name = f"budget-{subcategory.id}"
            description_field_name = f"description-{subcategory.id}"

            budget = request.POST.get(budget_field_name)
            description = request.POST.get(description_field_name)

            if budget:
                # Save the budget and description for the subdepartment along with the year
                allocation = BudgetAllocation.objects.create(
                    subcategory=subcategory,
                    budget=budget,
                    description=description,
                    year=year
                )
                allocation.save()
        cat_budget_set(category_id, year)
        subdep_budget_set(subdep_id, year)
        dep_budget_set(dep_id, year)
        # Redirect to a success page or perform any other action after saving the data
        return redirect('subcat_budget_allocation', category_id=category_id)

    context = {
        'dep_id': dep_id,
        'subdep_id': subdep_id,
        'category': category,
        'subcategories': subcategories,
    }

    return render(request, 'home/budget allocation/subcategories.html', context)


@login_required(login_url="/login/")
def subsubcat_budget_allocation(request, subcategory_id):
    subcategory = get_object_or_404(SubCategory, id=subcategory_id)
    cat_id = subcategory.category.id
    subdep_id = subcategory.category.subdepartment.id
    dep_id = subcategory.category.subdepartment.department.id
    subsubcategories = SubSubCategory.objects.filter(subcategory=subcategory)

    if request.method == 'POST':
        year = request.POST.get('year')  # Get the value of the year field
        for subsubcategory in subsubcategories:
            budget_field_name = f"budget-{subsubcategory.id}"
            description_field_name = f"description-{subsubcategory.id}"

            budget = request.POST.get(budget_field_name)
            description = request.POST.get(description_field_name)

            if budget:
                # Save the budget and description for the subdepartment along with the year
                allocation = BudgetAllocation.objects.create(
                    subsubcategory=subsubcategory,
                    budget=budget,
                    description=description,
                    year=year
                )
                allocation.save()
        subcat_budget_set(subcategory_id, year)
        cat_budget_set(cat_id, year)
        subdep_budget_set(subdep_id, year)
        dep_budget_set(dep_id, year)
        # Redirect to a success page or perform any other action after saving the data
        return redirect('subsubcat_budget_allocation', subcategory_id=subcategory_id)

    context = {
        'dep_id': dep_id,
        'subdep_id': subdep_id,
        'cat_id': cat_id,
        'subcategory': subcategory,
        'subsubcategories': subsubcategories,
    }

    return render(request, 'home/budget allocation/subsubcategories.html', context)


class depBudgetAllocationListView(ListView):
    model = Department
    template_name = 'home/budget allocation/management/department.html'
    context_object_name = 'departments'

    def get_queryset(self):
        # Check if the user is a superuser
        if self.request.user.is_superuser:
            # If user is superuser, return all departments
            return Department.objects.prefetch_related('budgetallocation_set').all()
        else:
            # If user is not superuser, return only the user's department
            return Department.objects.prefetch_related('budgetallocation_set').filter(id=self.request.user.department.id)   
        
    

from decimal import Decimal
@login_required(login_url="/login/")
def update_budget(request, budget_allocation_id):
    if request.method == 'POST' and request.is_ajax():
        budget_allocation = get_object_or_404(BudgetAllocation, id=budget_allocation_id)
        year = budget_allocation.year
        # Retrieve updated values from the POST data
        updated_year = request.POST.get('year')
        updated_budget = request.POST.get('budget')
        updated_description = request.POST.get('description')
        if budget_allocation.subdepartment:
            dep_id = budget_allocation.subdepartment.department.id
        elif budget_allocation.category:
            subdep_id = budget_allocation.category.subdepartment.id
            dep_id = budget_allocation.category.subdepartment.department.id
        elif budget_allocation.subcategory:
            cat_id = budget_allocation.subcategory.category.id
            subdep_id = budget_allocation.subcategory.category.subdepartment.id
            dep_id = budget_allocation.subcategory.category.subdepartment.department.id
        elif budget_allocation.subsubcategory:
            subcat_id = budget_allocation.subsubcategory.subcategory.id
            cat_id = budget_allocation.subsubcategory.subcategory.category.id
            subdep_id = budget_allocation.subsubcategory.subcategory.category.subdepartment.id
            dep_id = budget_allocation.subsubcategory.subcategory.category.subdepartment.department.id
            
        # Update the budget allocation with the new values
        budget_allocation.year = updated_year
        budget_allocation.budget = updated_budget
        budget_allocation.description = updated_description
        budget_allocation.save()
        if budget_allocation.subdepartment:
            dep_budget_set(dep_id,year)  
            dep_budget_set(dep_id,updated_year)
        elif budget_allocation.category:
            subdep_budget_set(subdep_id,year)  
            subdep_budget_set(subdep_id,updated_year)
            dep_budget_set(dep_id,year)  
            dep_budget_set(dep_id,updated_year)     
        elif budget_allocation.subcategory:
            cat_budget_set(cat_id,year)  
            cat_budget_set(cat_id,updated_year)
            subdep_budget_set(subdep_id,year)  
            subdep_budget_set(subdep_id,updated_year)
            dep_budget_set(dep_id,year)  
            dep_budget_set(dep_id,updated_year) 
        elif budget_allocation.subsubcategory:
            subcat_budget_set(subcat_id,year)  
            subcat_budget_set(subcat_id,updated_year)
            cat_budget_set(cat_id,year)  
            cat_budget_set(cat_id,updated_year)
            subdep_budget_set(subdep_id,year)  
            subdep_budget_set(subdep_id,updated_year)
            dep_budget_set(dep_id,year)  
            dep_budget_set(dep_id,updated_year) 
        

        return JsonResponse({'success': True})

    return JsonResponse({'success': False})

@login_required(login_url="/login/")
def delete_budget(request, budget_allocation_id):
    if request.method == 'POST' and request.is_ajax():
        budget_allocation = get_object_or_404(BudgetAllocation, id=budget_allocation_id)

        # Delete the budget allocation
        budget_allocation.delete()

        return JsonResponse({'success': True})

    return JsonResponse({'success': False})



class SubDepBudgetAllocationView(ListView):
    model = Department
    template_name = 'home/budget allocation/management/subdepartment.html'
    context_object_name = 'subdepartments'

    def get_queryset(self):
        department_id = self.kwargs.get('department_id')
        department = get_object_or_404(Department, id=department_id)
        return department.sub_departments.prefetch_related('budgetallocation_set').all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        department_id = self.kwargs.get('department_id')
        department = get_object_or_404(Department, id=department_id)
        context['main_department'] = department
        return context
    

class CatBudgetAllocationView(ListView):
    model = SubDepartment
    template_name = 'home/budget allocation/management/category.html'
    context_object_name = 'categories'

    def get_queryset(self):
        subdepartment_id = self.kwargs.get('subdepartment_id')
        subdepartment = get_object_or_404(SubDepartment, id=subdepartment_id)
        return subdepartment.categories.prefetch_related('budgetallocation_set').all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        subdepartment_id = self.kwargs.get('subdepartment_id')
        subdepartment = get_object_or_404(SubDepartment, id=subdepartment_id)
        context['main_subdepartment'] = subdepartment
        context['dep_id'] = subdepartment.department.id
        return context
    

class SubCatBudgetAllocationView(ListView):
    model = Category
    template_name = 'home/budget allocation/management/subcategory.html'
    context_object_name = 'subcategories'

    def get_queryset(self):
        category_id = self.kwargs.get('category_id')
        category = get_object_or_404(Category, id=category_id)
        return category.sub_categories.prefetch_related('budgetallocation_set').all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs.get('category_id')
        category = get_object_or_404(Category, id=category_id)
        context['main_category'] = category
        context['subdep_id'] = category.subdepartment.id
        context['dep_id'] = category.subdepartment.department.id
        return context

  
class SubSubCatBudgetAllocationView(ListView):
    model = SubCategory
    template_name = 'home/budget allocation/management/subsubcategory.html'
    context_object_name = 'subsubcategories'

    def get_queryset(self):
        subcategory_id = self.kwargs.get('subcategory_id')
        subcategory = get_object_or_404(SubCategory, id=subcategory_id)
        return subcategory.sub_subcategories.prefetch_related('budgetallocation_set').all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        subcategory_id = self.kwargs.get('subcategory_id')
        subcategory = get_object_or_404(SubCategory, id=subcategory_id)
        context['main_subcategory'] = subcategory
        context['cat_id'] = subcategory.category.id
        context['subdep_id'] = subcategory.category.subdepartment.id
        context['dep_id'] = subcategory.category.subdepartment.department.id
        return context

@login_required(login_url="/login/")   
def budget_comparison_dep(request):
    if request.method == 'POST':
        year1 = request.POST.get('year1')
        year2 = request.POST.get('year2')
        if request.user.is_superuser:
            departments = Department.objects.all().order_by('name')
        else :
            departments = Department.objects.filter(id=request.user.department.id)
        total1 = total2 = 0
        dep_budget_data = []
        for department in departments:
            try:
                budget1 = BudgetAllocation.objects.get(year=year1, department=department)
            except BudgetAllocation.DoesNotExist:
                budget1 = None

            try:
                budget2 = BudgetAllocation.objects.get(year=year2, department=department)
            except BudgetAllocation.DoesNotExist:
                budget2 = None

            if budget1:
                total1 += budget1.budget
            if budget2:
                total2 += budget2.budget
            dep_budget_data.append({
                'department': department,
                'budget1': budget1,
                'budget2': budget2,
            })

        context = {
            'dep_budget_data': dep_budget_data,
            'year1': year1,
            'year2': year2,
            'total1': total1,
            'total2': total2,
        }
        return render(request, 'home/budget allocation/compare/departments.html', context)

    return render(request, 'home/budget allocation/compare/year_input.html')

@login_required(login_url="/login/")
def budget_comparison_subdep(request, year1, year2, department_id):
    department = get_object_or_404(Department, id=department_id)
    subdepartments = department.sub_departments.all().order_by('name')
    subdep_budget_data = []
    total1 = total2 = 0
    for subdepartment in subdepartments:
        try:
            budget1 = BudgetAllocation.objects.get(year=year1, subdepartment=subdepartment)
        except BudgetAllocation.DoesNotExist:
            budget1 = None

        try:
            budget2 = BudgetAllocation.objects.get(year=year2, subdepartment=subdepartment)
        except BudgetAllocation.DoesNotExist:
            budget2 = None
        
        if budget1:
                total1 += budget1.budget
        if budget2:
                total2 += budget2.budget

        subdep_budget_data.append({
            'subdepartment': subdepartment,
            'budget1': budget1,
            'budget2': budget2,
        })

    context = {
        'subdep_budget_data': subdep_budget_data,
        'year1': year1,
        'year2': year2,
        'total1': total1,
        'total2': total2,
        'department': department,
    }
    return render(request, 'home/budget allocation/compare/subdepartments.html', context)


@login_required(login_url="/login/")
def budget_comparison_cat(request, year1, year2, subdepartment_id):
    subdepartment = get_object_or_404(SubDepartment, id=subdepartment_id)
    categories = subdepartment.categories.all().order_by('name')
    cat_budget_data = []
    total1 = total2 = 0
    for category in categories:
        try:
            budget1 = BudgetAllocation.objects.get(year=year1, category=category)
        except BudgetAllocation.DoesNotExist:
            budget1 = None

        try:
            budget2 = BudgetAllocation.objects.get(year=year2, category=category)
        except BudgetAllocation.DoesNotExist:
            budget2 = None
        
        if budget1:
                total1 += budget1.budget
        if budget2:
                total2 += budget2.budget

        cat_budget_data.append({
            'category': category,
            'budget1': budget1,
            'budget2': budget2,
        })

    context = {
        'cat_budget_data': cat_budget_data,
        'year1': year1,
        'year2': year2,
        'total1': total1,
        'total2': total2,
        'subdepartment': subdepartment,
        'department': subdepartment.department,
    }
    return render(request, 'home/budget allocation/compare/categories.html', context)

@login_required(login_url="/login/")
def budget_comparison_subcat(request, year1, year2, category_id):
    category = get_object_or_404(Category, id=category_id)
    subcategories = category.sub_categories.all().order_by('name')
    subcat_budget_data = []
    total1 = total2 = 0
    for subcategory in subcategories:
        try:
            budget1 = BudgetAllocation.objects.get(year=year1, subcategory=subcategory)
        except BudgetAllocation.DoesNotExist:
            budget1 = None

        try:
            budget2 = BudgetAllocation.objects.get(year=year2, subcategory=subcategory)
        except BudgetAllocation.DoesNotExist:
            budget2 = None
        
        if budget1:
                total1 += budget1.budget
        if budget2:
                total2 += budget2.budget

        subcat_budget_data.append({
            'subcategory': subcategory,
            'budget1': budget1,
            'budget2': budget2,
        })

    context = {
        'subcat_budget_data': subcat_budget_data,
        'year1': year1,
        'year2': year2,
        'total1': total1,
        'total2': total2,
        'category': category,
        'subdepartment': category.subdepartment,
        'department': category.subdepartment.department
    }
    return render(request, 'home/budget allocation/compare/subcategories.html', context)

@login_required(login_url="/login/")
def budget_comparison_subsubcat(request, year1, year2, subcategory_id):
    subcategory = get_object_or_404(SubCategory, id=subcategory_id)
    subsubcategories = subcategory.sub_subcategories.all().order_by('name')
    subsubcat_budget_data = []
    total1 = total2 = 0
    for subsubcategory in subsubcategories:
        try:
            budget1 = BudgetAllocation.objects.get(year=year1, subsubcategory=subsubcategory)
        except BudgetAllocation.DoesNotExist:
            budget1 = None

        try:
            budget2 = BudgetAllocation.objects.get(year=year2, subsubcategory=subsubcategory)
        except BudgetAllocation.DoesNotExist:
            budget2 = None
        
        if budget1:
                total1 += budget1.budget
        if budget2:
                total2 += budget2.budget

        subsubcat_budget_data.append({
            'subsubcategory': subsubcategory,
            'budget1': budget1,
            'budget2': budget2,
        })

    context = {
        'subsubcat_budget_data': subsubcat_budget_data,
        'year1': year1,
        'year2': year2,
        'total1': total1,
        'total2': total2,
        'subcategory': subcategory,
        'category': subcategory.category,
        'subdepartment': subcategory.category.subdepartment,
        'department': subcategory.category.subdepartment.department,
    }
    return render(request, 'home/budget allocation/compare/subsubcategories.html', context)