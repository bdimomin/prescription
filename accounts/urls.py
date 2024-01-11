from django.urls import path,include
from rest_framework.routers import DefaultRouter
from . views import *

router = DefaultRouter()
router.register('medicine', MedicineViewSet, basename='medicine')



urlpatterns = [
    path('api/', include(router.urls)),
    path('index/',index,name='index'),
    path('login/', login_view, name="login_user"),
    path('register/',registration, name="registration"),
    # path('prescriptions/',views.prescriptions, name="prescriptions"),
    path('<int:id>/profile/', profile_view, name="profile"),
    path('prescription/<int:id>/',prescriptionEdit, name="prescriptionEdit"),
    path('prescriptionpdf/<int:id>/',oneprescription, name="oneprescription"),
    path('prescriptionpdfprint/<int:id>/',prescriptionprint, name="prescriptionprint"),
    path('dashboard/', dashboard, name="dashboard"),
    path('generateprescription/<int:p_id>/', generateOldPrescription, name="dashboard2"),
    path('prescription/',prescription, name="prescription"),
    path('oldhistory/', oldpresscriptions, name="prescriptionsearch"),
    path('oldpatient/', oldpatient, name="oldpatient"),
    path("save/", medicinesave, name="medicinesave"),
    path('logout/',logout_user, name="logout"),
    
    
    path('useradmin-home/', home, name="superadminhome"),
    path('useradmin/new-client/', new_client, name="new_client"),
    path('useradmin/all-clients/', all_clients, name="all_clients"),
    path('useradmin/registration/', registry, name="superadminregistration"),
    path('useradmin/renewal/', renewal, name="renewal"),
    path('useradmin/expenses/', expenses, name="expenses"),
    
    path('useradmin/income-statement/', incomestatemts, name="superadminIncomeStatement"),
    path('useradmin/expense-statement/', expensestements, name="superadminExpenseStements"),
    path('useradmin/balance-statement/', balancestatements, name="superadminBalanceStatement"),
    path('useradmin/sms-bundle/', smsbundle, name="smsbundle"),
    
    path('useradmin/homepage/', homepage, name="homepage"),
    path('useradmin/homepage/<int:pk>/', homepageupdate, name="homepageupdate"),
    path('useradmin/home-delete/<int:pk>/', homedelete, name="homedelete"),
    
    path('useradmin/about/', aboutpage, name="aboutpage"),
    path('useradmin/about/<int:pk>/', aboutpageupdate, name="aboutpageupdate"),
    path('useradmin/about-delete/<int:pk>/', aboutdelete, name="aboutdelete"),
    
    path('useradmin/pricing/', pricingpage, name="pricingpage"),
    path('useradmin/pricing/<int:pk>/', pricingupdate, name="pricingupdate"),
    path('useradmin/pricing-delete/<int:pk>/', pricingdelete, name="pricingdelete"),
    
    
    path('useradmin/income-searching/', incomesearchingpage, name="incomesearchingpage"),
    path('useradmin/expense-searching/', expensesearchingpage, name="expensesearchingpage"),
    
]
    
    
