from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from . import forms
from . models import Emp, Employee, EmployeeInfo, user
import time

userExistsStatus = False

def logout(request):
    global userExistsStatus
    userExistsStatus = False
    try:
        del request.session['user_id']
    except KeyError:
        pass
    return redirect('index')

def delSession(request):
    global userExistsStatus
    userExistsStatus = False
    try:
        del request.session['user_id']
    except KeyError:
        pass
    return HttpResponse("Session terminated...")

def login(request):
    try:
        user = Emp.objects.get(username=request.POST['username']) 
        if user.password == request.POST['password']:
            request.session['user_id'] = user.id
            global userExistsStatus
            userExistsStatus = True
            return True
        else:
            delSession(request)
            return False   
    except Emp.DoesNotExist:
        delSession(request)
        return False

def index(request):
    if request.method == 'POST':
        loginForm = forms.LoginForms()
        if loginForm.is_valid:
            if login(request):
                return redirect('home')
            else:
                context = {'form' : loginForm, 'message' : 'Username and Password didn\'t match' }
                return render(request, 'emptimeclklogmgmt/index.html', context)
    else:
        delSession(request)
        loginForm = forms.LoginForms()
        context = {'form' : loginForm}
        return render(request, 'emptimeclklogmgmt/index.html', context)

def home(request):
    if userExistsStatus:
        if request.method == 'POST':
            return render(request,'emptimeclklogmgmt/homepage.html', {})
        else:
            users = Employee.objects.all()
            context = {'users' : users}
            return render(request,'emptimeclklogmgmt/homepage.html', context)
    else:
        return HttpResponse('Login again using the link: \'http://127.0.0.1:8000/timeclock/\' ')

def register(request):
    if request.method == 'POST':
        registerForm = forms.RegisterForms()
        if registerForm.is_valid:
            '''
            empObj = Emp(
                username=request.POST['username'], 
                password=request.POST['password'], 
                recovery_answer=request.POST['recovery_answer'], 
                recovery_email=request.POST['recovery_email'],
                first_name=request.POST['first_name'], 
                middle_name=request.POST['middle_name'], 
                last_name=request.POST['last_name'], 
                phone_number=request.POST['phone_number']
            )
            empObj.save()
            '''
        
            empObj = Employee(
                username=request.POST['username'], 
                password=request.POST['password'], 
                recovery_answer=request.POST['recovery_answer'], 
                recovery_email=request.POST['recovery_email']
            )
            empObj.save()
            empInfoObj = EmployeeInfo( 
                employee=empObj,
                first_name=request.POST['first_name'], 
                middle_name=request.POST['middle_name'], 
                last_name=request.POST['last_name'], 
                phone_number=request.POST['phone_number']
            )
            empInfoObj.save()

        return redirect('index')
    registerForms = forms.RegisterForms()
    context = {'user' : registerForms}
    return render(request, 'emptimeclklogmgmt/registeruser.html', context)