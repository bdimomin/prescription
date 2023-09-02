from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm

from .models import CustomUser, Prescription, PrescriptionMedicine, DoctorProfile



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