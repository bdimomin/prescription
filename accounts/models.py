from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

import barcode
from barcode.writer import ImageWriter
from io import BytesIO
from django.core.files import File

class UserManager(BaseUserManager):
    def create_user(self, name, email, phone, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not phone:
            raise ValueError('Users must have a phone number')

        user= self.model(
            email= self.normalize_email(email),
            name=name,
            phone=phone,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,name, email, phone, password=None):
        user = self.create_user(
            email= self.normalize_email(email),
            name=name,
            phone=phone,
            password=password
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user

class CustomUser(AbstractBaseUser):
    name= models.CharField(max_length=255)
    email= models.EmailField(max_length=100,unique=True)
    phone= models.CharField(max_length=15,unique=True)


    #required fields
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    created_date=models.DateTimeField(auto_now_add=True)
    modified_date=models.DateTimeField(auto_now=True)

    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superadmin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name','phone']

    objects=UserManager()

    def __str__(self):
        return self.name

    def has_perm(self,perm,obj=None):
        return True

    def has_module_perms(self,app_label):
        return True


class Prescription(models.Model):
    patient_gender =  (
        ('Male','Male'),
        ('Female','Female'),
    )
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    p_id = models.CharField(max_length=10, blank=True, null=True)
    patient_name = models.CharField(max_length=100)
    patient_age = models.IntegerField()
    patient_sex = models.CharField(max_length=7, choices=patient_gender)
    patient_address = models.CharField(max_length=255)
    patient_mobile = models.CharField(max_length=15)
    patient_weight = models.CharField(max_length=10,null=True, blank=True)

    disease = models.CharField(max_length=155, blank=True, null=True)
    complaint     = models.TextField(blank=True, null=True)
    BP = models.CharField(blank=True, null=True,max_length=20)
    Pulse =  models.CharField(blank=True, null=True,max_length=20)
    Temp =  models.CharField(blank=True, null=True,max_length=20)
    Sp02= models.CharField(blank=True, null=True,max_length=20)
    RBS = models.CharField(blank=True, null=True,max_length=20)
    Heart = models.CharField(blank=True, null=True,max_length=20)
    others = models.TextField(blank=True, null=True)
    ix = models.TextField(blank=True, null=True)
   

    created_date=models.DateField(auto_now_add=True)
    modified_date=models.DateTimeField(auto_now=True)

    def __str__ (self):
        return self.patient_name

    


class DoctorProfile(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    degree = models.CharField(max_length=100,null=True, blank=True)
    degree_description = models.CharField(max_length=200,null=True, blank=True)
    degree_year = models.CharField(max_length=100,null=True, blank=True)
    degree_university = models.CharField(max_length=100,null=True, blank=True)
    degree_country = models.CharField(max_length=100,null=True, blank=True)

    def __str__(self):
        return self.degree

class Medicine(models.Model):
    types = models.CharField(max_length=255, blank=True, null=True)
    name=models.CharField(max_length=255, blank=True, null=True)
    generic_name = models.CharField(max_length=255, blank=True, null=True)
    strength = models.CharField(max_length=255, blank=True, null=True)
    company_name = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name


class PrescriptionMedicine(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    dose = models.CharField(max_length=100, null=True, blank=True)
    duration = models.CharField(max_length=3, null=True, blank=True)
    day_month = models.CharField(max_length=20, null=True, blank=True)
    before_after = models.CharField(max_length=20, null=True, blank=True)
    prescription = models.ForeignKey(Prescription, on_delete=models.CASCADE, null=True, blank=True)

    created_date=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


