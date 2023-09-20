from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm

from .models import *



class CustomUserForm(UserCreationForm):
    class Meta:
        model=CustomUser
        fields=['name','email','phone','password1','password2']

        
class UserLoginForm(forms.ModelForm):
    email = forms.EmailField()
    password = forms.CharField(label="Password",widget=forms.PasswordInput)
    class Meta:
        model=CustomUser
        fields=['email', 'password']
        
    def clean(self):
        if self.is_valid():
            email=self.cleaned_data['email']
            password=self.cleaned_data['password']
            
            if not authenticate(email=email,password=password):
                raise forms.ValidationError("Invalid Credentials")
            
class PrescriptionForm(forms.ModelForm):
    class Meta:
        model=Prescription
        exclude =['user']
        widgets = {
            'p_id': forms.HiddenInput(attrs={'type': 'hidden'}),
        }
        
   
class PrescriptioinMedicineForm(forms.ModelForm):
    class Meta:
        model = PrescriptionMedicine
        exclude =['created_date']
        
class DoctorProfileForm(forms.ModelForm):
    class Meta:
        model = DoctorProfile
        exclude = ['user']
        
        
        
class RegistrationForm(forms.ModelForm):
    class Meta:
        model = Registration
        fields=['name','email','mobile','amount',]
class RenewalForm(forms.ModelForm):
    class Meta:
        model = Renewal
        fields=['name','amount']
        
class ExpensesForm(forms.ModelForm):
    class Meta:
        model = Expenses
        fields=['purpose','amount']
        
class SuperAdminIncomeStatementForm(forms.ModelForm):
    class Meta:
        model = SuperAdminIncomeStatement
        fields = '__all__'
        
    def __init__(self, user=None, **kwargs):
        super(SuperAdminIncomeStatementForm, self).__init__(**kwargs)
        if user:
            self.fields['client'].queryset =CustomUser.objects.filter(is_superadmin=0)
class SuperAdminExpenseStatementForm(forms.ModelForm):
    class Meta:
        model = SuperAdminExpenseStatement
        fields = '__all__'
        
    def __init__(self, user=None, **kwargs):
        super(SuperAdminExpenseStatementForm, self).__init__(**kwargs)
        if user:
            self.fields['client'].queryset =CustomUser.objects.filter(is_superadmin=0)
class SMSBundleForm(forms.ModelForm):
    class Meta:
        model = SMSBundle
        fields = '__all__'
        
    def __init__(self, user=None, **kwargs):
        super(SMSBundleForm, self).__init__(**kwargs)
        if user:
            self.fields['client'].queryset =CustomUser.objects.filter(is_superadmin=0)