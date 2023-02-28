from django.http import HttpResponse
from django.shortcuts import render

def home_page(request):
    return render(request,"index.html",{"title":"This is the home page!"})


#def home_page(request):
   # return HttpResponse("<h1>Hellow World!</h1>")

