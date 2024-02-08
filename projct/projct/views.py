from django.shortcuts import render,HttpResponse

def home():
    return HttpResponse("Home page")