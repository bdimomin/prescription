from django.shortcuts import render

from accounts.models import *

def homepage(request):
    try:
        homepage = Homepage.objects.order_by('-id')[0]
        return render(request, 'frontpage/homepage.html',{'homepage': homepage})
    except:
        return render(request, 'frontpage/homepage.html')


def about(request):
    try:
        aboutpage = Aboutpage.objects.order_by('-id')[0]
        return render(request, 'frontpage/about.html',{'aboutpage':aboutpage})
    except:
        return render(request, 'frontpage/about.html')

def pricing(request):
    try:
        pricingpage = Pricingpage.objects.order_by('-id')[0]
        return render(request, 'frontpage/pricing.html',{'pricingpage':pricingpage})
    except:
        return render(request, 'frontpage/pricing.html')
