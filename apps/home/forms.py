from django import forms
from .models import Department, SubDepartment, Category, SubCategory, SubSubCategory, BudgetAllocation

class BudgetAllocationForm(forms.ModelForm):
    class Meta:
        model = BudgetAllocation
        fields = ['budget','description']
        
class SubSubCategoryForm(forms.ModelForm):
    class Meta:
        model = SubSubCategory
        fields = '__all__'

class SubCategoryForm(forms.ModelForm):
    class Meta:
        model = SubCategory
        fields = '__all__'

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'

class SubDepartmentForm(forms.ModelForm):
    class Meta:
        model = SubDepartment
        fields = '__all__'
# class DepartmentForm(forms.Form):
#     name = forms.CharField(max_length=100)
#     budget = forms.DecimalField(:max_digits=10, decimal_places=2)
#     year = forms.IntegerField()
#     sub_departments = forms.formset_factory(SubDepartmentForm, extra=1, min_num=0)

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = '__all__'