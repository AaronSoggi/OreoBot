from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import studentForm

import time
import chatbot
import json


@login_required(login_url='login')
def dashboard(request):
    return render(request, 'AnxietyBot.html')

def getResponse(request):
    userMessage = request.GET.get('userMessage')
    chat_Response = str(chatbot.chat(userMessage))
    time.sleep(1)
    return HttpResponse(chat_Response)

def register(request):

    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        if request.method == "POST":
            registration_form = studentForm(request.POST) # here we are storing the data from student form and storing it in form
            if  registration_form.is_valid(): #saving it to database
                registration_form.save() # saving form with data 
                username =  registration_form.cleaned_data.get('username') # gets the user name from a dictionary
                messages.success(request, f'Hi {username} your account has been created succesfully')
                return redirect('login') # going back to login page
        else:
             registration_form = studentForm()

    return render(request, 'registration.html', {'form':  registration_form})

def studentlogin(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        if request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('password')

            student = authenticate(request, username=username, password=password)

            if student is not None:
                login(request, student)
                return redirect('dashboard')
            elif len(username) == 0 and len(password) == 0 or len(username) == 0 or len(password) == 0 :
                messages.info(request, f'Please ensure that both fields have been filled')   
            else:
                messages.info(request, f'Login credentials are incorrect, please try again')     
            
                   
    context = {}
    return render(request, 'login.html', context)

def studentlogout(request):
    logout(request)
    return redirect('login')


def about(request):
    return render(request, 'about.html')

def advice(request):
    return render(request, 'advice.html')









