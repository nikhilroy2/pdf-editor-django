from django.shortcuts import render

# Create your views here.

def Index(request):
    return render(request, 'index.html')

def Watermark(request):
    return render(request, 'watermark.html')