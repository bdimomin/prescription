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
    path('dashboard/', views.dashboard, name="dashboard"),
    path('prescription/',views.prescription, name="prescription"),
    path("save/", views.medicinesave, name="medicinesave"),
    path('logout/',views.logout_user, name="logout"),
]
    
    
