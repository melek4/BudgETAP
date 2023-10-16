# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from apps.home import views

urlpatterns = [

    # The home page
    path('', views.index, name='home'),

    # Matches any html file
    # re_path(r'^.*\.*', views.pages, name='pages'),


    path('dep_management/', views.dep_management, name='dep_management'),
    path('dep_management/create_department/', views.create_department, name='create_department'),
    path('dep_management/modify_department/<int:department_id>/', views.modify_department, name='modify_department'),
    path('dep_management/delete_department/<int:department_id>/', views.delete_department, name='delete_department'),

    path('subdep_management/<int:department_id>/', views.subdep_management, name='subdep_management'),
    path('subdep_management/<int:department_id>/create_subdepartment/', views.create_subdepartment, name='create_subdepartment'),
    path('subdep_management/<int:department_id>/modify_subdepartment/<int:subdepartment_id>/', views.modify_subdepartment, name='modify_subdepartment'),
    path('subdep_management/<int:department_id>/delete_subdepartment/<int:subdepartment_id>/', views.delete_subdepartment, name='delete_subdepartment'),
    
    path('cat_management/<int:subdepartment_id>/', views.cat_management, name='cat_management'),
    path('cat_management/<int:subdepartment_id>/create_category/', views.create_category, name='create_category'),
    path('cat_management/<int:subdepartment_id>/modify_category/<int:category_id>/', views.modify_category, name='modify_category'),
    path('cat_management/<int:subdepartment_id>/delete_category/<int:category_id>/', views.delete_category, name='delete_category'),

    path('subcat_management/<int:category_id>/', views.subcat_management, name='subcat_management'),
    path('subcat_management/<int:category_id>/create_subcategory/', views.create_subcategory, name='create_subcategory'),
    path('subcat_management/<int:category_id>/modify_subcategory/<int:subcategory_id>/', views.modify_subcategory, name='modify_subcategory'),
    path('subcat_management/<int:category_id>/delete_subcategory/<int:subcategory_id>/', views.delete_subcategory, name='delete_subcategory'),

    path('subsubcat_management/<int:subcategory_id>/', views.subsubcat_management, name='subsubcat_management'),
    path('subsubcat_management/<int:subcategory_id>/create_subsubcategory/', views.create_subsubcategory, name='create_subsubcategory'),
    path('subsubcat_management/<int:subcategory_id>/modify_subsubcategory/<int:subsubcategory_id>/', views.modify_subsubcategory, name='modify_subsubcategory'),
    path('subsubcat_management/<int:subcategory_id>/delete_subsubcategory/<int:subsubcategory_id>/', views.delete_subsubcategory, name='delete_subsubcategory'),

    path('dep_budget_allocation/', views.dep_budget_allocation, name='dep_budget_allocation'),
    path('subdep_budget_allocation/<int:department_id>/', views.subdep_budget_allocation, name='subdep_budget_allocation'),
    path('cat_budget_allocation/<int:subdepartment_id>/', views.cat_budget_allocation, name='cat_budget_allocation'),
    path('subcat_budget_allocation/<int:category_id>/', views.subcat_budget_allocation, name='subcat_budget_allocation'),
    path('subsubcat_budget_allocation/<int:subcategory_id>/', views.subsubcat_budget_allocation, name='subsubcat_budget_allocation'),

    path('departments/', views.depBudgetAllocationListView.as_view(), name='depBudgetAllocationListView'),
    path('update_budget/<int:budget_allocation_id>/', views.update_budget, name='update_budget'),
    path('delete_budget/<int:budget_allocation_id>/', views.delete_budget, name='delete_budget'),

    path('departments/<int:department_id>/subdepartments/', views.SubDepBudgetAllocationView.as_view(), name='SubDepBudgetAllocationView'),
    path('subdepartments/<int:subdepartment_id>/categories/', views.CatBudgetAllocationView.as_view(), name='CatBudgetAllocationView'),
    path('categories/<int:category_id>/subcategories/', views.SubCatBudgetAllocationView.as_view(), name='SubCatBudgetAllocationView'),
    path('subcategories/<int:subcategory_id>/subsubcategories/', views.SubSubCatBudgetAllocationView.as_view(), name='SubSubCatBudgetAllocationView'),

    path('budget-comparison-dep/', views.budget_comparison_dep, name='budget_comparison_dep'),
    path('budget-comparison-subdep/<int:year1>/<int:year2>/<int:department_id>/', views.budget_comparison_subdep, name='budget_comparison_subdep'),
    path('budget-comparison-cat/<int:year1>/<int:year2>/<int:subdepartment_id>/', views.budget_comparison_cat, name='budget_comparison_cat'),
    path('budget-comparison-subcat/<int:year1>/<int:year2>/<int:category_id>/', views.budget_comparison_subcat, name='budget_comparison_subcat'),
    path('budget-comparison-subsubcat/<int:year1>/<int:year2>/<int:subcategory_id>/', views.budget_comparison_subsubcat, name='budget_comparison_subsubcat'),

]
