from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return render(request, 'web/index.html',{})

def buyer_inquiry(request): 
    return render(request, 'web/buyer_inquiry.html',{})

def vendor_inquiry(request): 
    return render(request, 'web/vendor_inquiry.html',{})
