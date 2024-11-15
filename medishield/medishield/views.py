# created by Rizwan
from django.http import HttpResponse
from django.shortcuts import render
import datetime

def home(request):
    x=datetime.datetime.now()
    params={'date':x}
    return render(request,'home.html',params)

def suppliers(request):
    return render(request, 'suppliers.html')


def new_supp(request):
    return render (request, 'new_supp.html')