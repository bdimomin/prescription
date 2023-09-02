import os
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from accounts.serializers import MedicineSerializer
from django.shortcuts import render,redirect
from django.contrib.auth import login,logout, authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from .forms import CustomUserForm,UserLoginForm, PrescriptionForm, PrescriptioinMedicineForm,DoctorProfileForm
from .models import Prescription, CustomUser, Medicine, PrescriptionMedicine, DoctorProfile
from django.template.loader import render_to_string
from weasyprint import HTML, CSS
import tempfile
from datetime import date
from rest_framework.permissions import IsAuthenticated


@login_required
def dashboard(request):
    user = request.user
    patient = Prescription.objects.filter(user=user).order_by('-pk')[0]
    patient_id=patient.id
    prescription = PrescriptionForm(instance=patient)
    medicine = PrescriptionMedicine.objects.filter(prescription=patient_id)
    context={
        'prescription':prescription,
        'patient_id':patient_id,
        'medicine':medicine
       
    }
    
    if request.method == 'POST':
      
      prescription = PrescriptionForm(request.POST, instance=patient)
      if prescription.is_valid():
          prescription.instance.user = request.user
          prescription.save()
          return redirect('prescription')
    
    return render(request, 'doctor/dashboard.html',context)
@login_required
def prescriptionEdit(request, id):
    patient_id=id
    patient = Prescription.objects.get(id=patient_id)
    prescription = PrescriptionForm(instance=patient)
    medicine = PrescriptionMedicine.objects.filter(prescription=patient_id)
    context={
        'prescription':prescription,
        'patient_id':patient_id,
        'medicine':medicine
       
    }
    
    if request.method == 'POST':
        patient_id=id
        patient = Prescription.objects.get(id=patient_id)
        prescription = PrescriptionForm(request.POST,instance=patient)
        if prescription.is_valid():
            prescription.save()
            return redirect('prescription')
        
    return render(request, 'doctor/dashboard.html',context)

@login_required
def oldpresscriptions(request):
        
        
    if request.method == 'POST':
        p_id = request.POST.get('p_id')
        name = request.POST.get('name')
        age = request.POST.get('age')
        gender = request.POST.get('gender')
        address = request.POST.get('address')
        mobile = request.POST.get('mobile')
        weight = request.POST.get('weight')
        print(p_id, name, age, gender, address, mobile, weight)
        user= CustomUser.objects.get(id=request.user.id)
       
        try:
            Prescription.objects.create(user=user, p_id=p_id, patient_name=name, patient_age=age, patient_sex=gender, 
                                           patient_address=address,patient_mobile=mobile,patient_weight=weight).save()
            return redirect('dashboard')
        except:
            print("ERROR")
       
        
    else:
        pass
    
    
    try:
        p_id = request.POST.get('p_id')
        profile = CustomUser.objects.get(id=request.user.id)
        patient = Prescription.objects.filter(p_id=p_id)
        patient_details = Prescription.objects.filter(p_id=p_id).order_by('-pk')[0]
        patient_id=patient_details.id
        
    except:
        patient_details="Not found"
        patient_id="ID not found"
        
    context={
        'patient':patient,
        'profile':profile,
        'patient_details':patient_details,
        'patient_id':patient_id
    }
    
    return render(request, 'doctor/oldprescriptions.html',context)
        
        
       
    


@login_required
def generateOldPrescription(request,p_id):
    # prescription= Prescription.objects.filter(p_id=p_id).order_by('-pk')[0]
    # patient_id=prescription.id
    # print(patient_id)
    
    
    if request.method == 'POST':
        user = request.user.id
        patient_id = request.POST.get('patient_id')
        name = request.POST.get('name')
        age = request.POST.get('age')
        gender = request.POST.get('gender')
        address = request.POST.get('address')
        mobile= request.POST.get('mobile')
        weight = request.POST.get('weight')
        disease = request.POST.get('disease')
        complaint = request.POST.get('complaint')
        bp = request.POST.get('bp')
        pulse = request.POST.get('pulse')
        temp = request.POST.get('temp')
        sp02 = request.POST.get('sp02')
        rbs = request.POST.get('rbs')
        heart = request.POST.get('heart')
        others = request.POST.get('others')
        ix = request.POST.get('ix')
        
        
        prescription= Prescription.objects.get(id=patient_id)
        
        id = request.user
        user= CustomUser.objects.get(id=id)
       
        Prescription.objects.create(user=user, p_id=patient_id, patient_name=name, patient_age=age, patient_sex=gender, 
                                           patient_address=address,patient_mobile=mobile,patient_weight=weight,disease=disease, 
                                           complaint=complaint,BP=bp,Pulse=pulse,Temp=temp,Sp02=sp02, 
                                           RBS=rbs, Heart=heart,others=others,ix=ix).save()
        return redirect('prescription')
        
        
    return render(request, 'doctor/dashboard2.html', {'prescription':prescription})


@login_required
def oldpatient(request):
    user = request.user.id 
    p_id = request.POST.get('p_id')
    prescription= Prescription.objects.filter(p_id=p_id).order_by('-pk')[0]
    patient_id=prescription.id
    
    if request.method == 'POST':
       
        name = request.POST.get('name')
        age = request.POST.get('age')
        gender = request.POST.get('gender')
        address = request.POST.get('address')
        mobile= request.POST.get('mobile')
        weight = request.POST.get('weight')
        
        user= CustomUser.objects.get(id=request.user.id)
        
        pres = Prescription.objects.create(user=user, p_id=p_id, patient_name=name, patient_age=age, patient_sex=gender, 
                                            patient_address=address,patient_mobile=mobile,patient_weight=weight).save()

    
    return render(request, 'doctor/dashboard2.html', {'prescription':prescription,'patient_id':patient_id})


@login_required
def prescription(request):
    
   
    profile = CustomUser.objects.get(id=request.user.id)
    prescription= PrescriptionForm()
    prescriptions= Prescription.objects.filter(user=request.user, p_id__isnull=False).order_by('-id')[:5]
    try:
        last_id = Prescription.objects.all().order_by('-id')[0]
        serial_id= last_id.id+1
    except:
        serial_id = 1
        
    
    da = date.today()
    year = da.strftime("%y")
    month = da.strftime("%m")
    today = da.strftime("%d")
    unique_id= year+month+today+str(serial_id).zfill(3)
    doctorprofile = DoctorProfile.objects.filter(user= request.user)
    context={
        'prescription':prescription,
        'prescriptions':prescriptions,
        'profile':profile,
        'doctorprofile':doctorprofile
       
    }
    if request.method == 'POST':
        prescription = PrescriptionForm(request.POST)
        if prescription.is_valid():
            prescription.instance.user = request.user
            prescription.instance.p_id = unique_id
            prescription.save()
            return redirect('dashboard')
    return render(request, 'doctor/prescriptions.html',context)
    
    
    
    
    
    
   
        
            
    



    

def registration(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    context={}
    
    if request.method=="POST":
        form=CustomUserForm(request.POST)
        if form.is_valid():
            user= form.save()
            login(request, user)
            return redirect('prescription')
        context['register_form']=form
    else:
        form= CustomUserForm()
        context['register_form']=form
        
    return render(request,'registration/sign_up.html',context)

def login_view(request):
    if request.user.is_authenticated:
        return redirect('prescription') 

    login_form = UserLoginForm()
    if request.method=="POST":
        login_form= UserLoginForm(request.POST)
        if login_form.is_valid():
            email=request.POST['email']
            password=request.POST['password']
            user=authenticate(request,email=email,password=password)
            
            if user is not None:
                login(request,user)
                return redirect('prescription')
            else:
                return redirect('login_user')
    else:
        login_form= UserLoginForm()
    return render(request,'registration/login.html',{'login_form':login_form})

@login_required
def prescriptions(request):
    prescription= PrescriptionForm()
   
    context={
        'prescription':prescription,
        'prescriptions':prescriptions,
       
    }
    prescriptions= Prescription.objects.filter(user=request.user)
   
    return render(request,'doctor/prescriptions.html', context)

@login_required
def oneprescription(request, *args, **kwargs):
    id = kwargs.get('id')
    prescriptions= Prescription.objects.get(id=id)
    medicines = PrescriptionMedicine.objects.filter(prescription=id)
    doctor = CustomUser.objects.get(id=prescriptions.user_id)
    Doctorprofile = DoctorProfile.objects.filter(user=prescriptions.user_id)
    
    html_string = render_to_string('doctor/prescriptionpdf.html',{
        "prescriptions":prescriptions,'doctor':doctor, 'medicines':medicines,'Doctorprofile':Doctorprofile})
    base_url = os.path.dirname(os.path.realpath(__file__))
    html = HTML(string=html_string,base_url=base_url)
    
    result = html.write_pdf()
    
    response = HttpResponse(content_type='application/pdf;')
    response['Content-Disposition'] = 'inline; filename=prescription.pdf'
    response['Content-Transfer-Encoding'] = 'binary'
    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output.seek(0)
        response.write(output.read())

    return response


@login_required
def prescriptionprint(request, *args, **kwargs):
    id = kwargs.get('id')
    prescriptions= Prescription.objects.get(id=id)
    medicines = PrescriptionMedicine.objects.filter(prescription=id)
    doctor = CustomUser.objects.get(id=prescriptions.user_id)
    Doctorprofile = DoctorProfile.objects.filter(user=prescriptions.user_id)
    
    html_string = render_to_string('doctor/prescriptionpdf2.html',{
        "prescriptions":prescriptions,'doctor':doctor, 'medicines':medicines,'Doctorprofile':Doctorprofile})
    base_url = os.path.dirname(os.path.realpath(__file__))
    html = HTML(string=html_string,base_url=base_url)
    
    result = html.write_pdf()
    
    response = HttpResponse(content_type='application/pdf;')
    response['Content-Disposition'] = 'inline; filename=prescription.pdf'
    response['Content-Transfer-Encoding'] = 'binary'
    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output.seek(0)
        response.write(output.read())

    return response


def logout_user(request):
    logout(request)
    return redirect('login_user')

    
class MedicineViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = MedicineSerializer
    queryset = Medicine.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['name']
    
@login_required
def medicinesave(request):
    if request.method == "POST":
        prescription_id = request.POST.get("patient_id")
        
        prescription = Prescription.objects.get(id=prescription_id)
        form = PrescriptioinMedicineForm(request.POST, instance=prescription)
        if form.is_valid():
            medicine_name = request.POST.get("medicine_name")
            dose = request.POST.get("medicine_dose")
            duration = request.POST.get("medicine_duration")
            day_month = request.POST.get("day_month")
            before_after = request.POST.get("before_after")
            
            
            
            prescription_medicine = PrescriptionMedicine(name=medicine_name,dose=dose,duration=duration,day_month=day_month,before_after=before_after,prescription=prescription)
            prescription_medicine.save()
            medicines = PrescriptionMedicine.objects.filter(prescription=prescription).values()
            medicine_list = list(medicines)
            return JsonResponse({'status':'save',
                                 'medicine_list':medicine_list
                
                                 
                                 })
        else:
            return JsonResponse({'status':0})

@login_required
def profile_view(request, id):
    profile = CustomUser.objects.get(id=id)
    form = DoctorProfileForm()
    Doctorprofile = DoctorProfile.objects.filter(user=id)
    context={
        'profile':profile,
        'form':form,
        'Doctorprofile':Doctorprofile
    }
    if request.method == 'POST':
        form = DoctorProfileForm(request.POST)
        if form.is_valid():
            form.instance.user = request.user
            form.save()
    return render(request, 'doctor/doctorprofile.html', context)
        

    

