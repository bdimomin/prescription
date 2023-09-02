from django.urls import path,include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('medicine', views.MedicineViewSet, basename='medicine')



urlpatterns = [
    path('api/', include(router.urls)),
    path('', views.login_view, name="login_user"),
    path('register/',views.registration, name="registration"),
    # path('prescriptions/',views.prescriptions, name="prescriptions"),
    path('<int:id>/profile/', views.profile_view, name="profile"),
    path('prescription/<int:id>/',views.prescriptionEdit, name="prescriptionEdit"),
    path('prescriptionpdf/<int:id>/',views.oneprescription, name="oneprescription"),
    path('prescriptionpdfprint/<int:id>/',views.prescriptionprint, name="prescriptionprint"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('generateprescription/<int:p_id>/', views.generateOldPrescription, name="dashboard2"),
    path('prescription/',views.prescription, name="prescription"),
    path('oldhistory/', views.oldpresscriptions, name="prescriptionsearch"),
    path('oldpatient/', views.oldpatient, name="oldpatient"),
    path("save/", views.medicinesave, name="medicinesave"),
    path('logout/',views.logout_user, name="logout"),
]
    
    
