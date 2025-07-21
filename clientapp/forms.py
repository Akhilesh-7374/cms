from django import forms
from .models import Client
from .models import SupportCall
from .models import AllPayments
from .models import AllUsers
from .models import Branch

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = '__all__'
        widgets = {
            'password': forms.PasswordInput()}

class SupportCallForm(forms.ModelForm):
    class Meta:
        model = SupportCall
        fields = '__all__'
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 4}),}

class AllPaymentsForm(forms.ModelForm):
    class Meta:
        model = AllPayments
        fields = '__all__'


class BranchForm(forms.ModelForm):
    class Meta:
        model = Branch
        fields = [
            'client', 'branch_name', 'branch_code', 'contact_name', 'contact_number',
            'address','weblink','username', 'number_of_students', 'description'
        ]
        widgets = {
            'address': forms.Textarea(attrs={'rows': 2}),
            'description': forms.Textarea(attrs={'rows': 2}),
        }

class AllUsersForm(forms.ModelForm):
    class Meta:
        model = AllUsers
        fields = ['user_id', 'password', 'role']
        
