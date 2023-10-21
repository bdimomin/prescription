from django.urls import path
from .views import *

urlpatterns = [
    path('', homepage , name='homepagecontent'),
    path('about/', about , name='about'),
    path('pricing/', pricing , name='pricing'),
]