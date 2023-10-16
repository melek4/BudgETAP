# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

# Create your models here.

class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)


    def __str__(self):
        return self.name

class SubDepartment(models.Model):
    name = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='sub_departments')
    
    def __str__(self):
        return self.name
    
    class Meta:
        unique_together = ['name', 'department']

class Category(models.Model):
    name = models.CharField(max_length=100)
    subdepartment  = models.ForeignKey(SubDepartment, on_delete=models.CASCADE, related_name='categories')

    def __str__(self):
        return self.name
    
    class Meta:
        unique_together = ['name', 'subdepartment']

class SubCategory(models.Model):
    name = models.CharField(max_length=100)
    category  = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='sub_categories')

    def __str__(self):
        return self.name
    
    class Meta:
        unique_together = ['name', 'category']

class SubSubCategory(models.Model):
    name = models.CharField(max_length=100)
    subcategory  = models.ForeignKey(SubCategory, on_delete=models.CASCADE, related_name='sub_subcategories')

    def __str__(self):
        return self.name
    
    class Meta:
        unique_together = ['name', 'subcategory']


class BudgetAllocation(models.Model):
    year = models.PositiveIntegerField()
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=300, null=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True)
    subdepartment = models.ForeignKey(SubDepartment, on_delete=models.CASCADE, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, null=True)
    subsubcategory = models.ForeignKey(SubSubCategory, on_delete=models.CASCADE, null=True)


    def __str__(self):
        return f"{self.year} - {self.get_allocated_item()} - Budget: {self.budget}"
    
    def clean(self):
        fields = ['department', 'subdepartment', 'category', 'subcategory', 'subsubcategory']
        field_values = [getattr(self, field) for field in fields]
        num_fields_with_value = sum(bool(field_value) for field_value in field_values)

        if num_fields_with_value != 1:
            raise ValidationError('Only one foreign key field should have a value.')

    def get_allocated_item(self):
        if self.department:
            return f"Department: {self.department.name}"
        elif self.subdepartment:
            return f"SubDepartment: {self.subdepartment.name}"
        elif self.category:
            return f"Category: {self.category.name}"
        elif self.subcategory:
            return f"SubCategory: {self.subcategory.name}"
        elif self.subsubcategory:
            return f"SubSubCategory: {self.subsubcategory.name}"
        else:
            return "Unknown"

    def get_related_model(self):
        if self.department:
            return self.department
        elif self.subdepartment:
            return self.subdepartment
        elif self.category:
            return self.category
        elif self.subcategory:
            return self.subcategory
        elif self.subsubcategory:
            return self.subsubcategory
        else:
            return None

    class Meta:
        unique_together = [
            ('year', 'department'),
            ('year', 'subdepartment'),
            ('year', 'category'),
            ('year', 'subcategory'),
            ('year', 'subsubcategory'),
        ]