from django.shortcuts import render
from django.http import HttpResponse

from django.shortcuts import render, redirect
from django.shortcuts import redirect
import subprocess as sp
from .forms import User
from .forms import EmployeeForm
from .forms import SMSJobForm
from .forms import ScriptJobForm
from .forms import ScriptJobForm_PHP
from .forms import runAccountForm
from .forms import smsAccountForm
#from .forms import PatientForm
from .forms import UserForm

from .forms import DateForm

from .models import Employee
from .models import SMSJob
from .models import ScriptJob
from .models import Runtime_Account
from .models import Text_Account
#from .models import Patient
from .models import User
from .models import ScriptJobType
from .models import UserType
from .models import RecurrentType

import matplotlib.pyplot as plt
import io
import urllib, base64

import subprocess

import requests
import os
from datetime import date
from random import randint
from django.contrib import messages
from django.contrib.auth.hashers import make_password

FirstName = "Test"
LastName = "Test"
mobile = '0000000000'
Email = 'Test@mail.com'
Username = 'testUserName'
Password = 'omicron0000'

job_python='Python'
job_php='PHP'

manualSet='Manually Set Date and Time'
everyMinute='Every Minute'
everyHour='Every Hour'


def access_session_data(request):
    response = ""
    if request.session.get('user_id'):
        user_id = request.session.get('user_id')
        response += "User Id : {0} <br>".format(user_id)
    if request.session.get('team'):
        team = request.session.get('team')
        response += "Team : {0} <br>".format(team)

    if not response:
        return HttpResponse("No session data")
    else:
        return HttpResponse(response)


def delete_session_data(request):
    try:
        del request.session['user_id']
        del request.session['team']
    except KeyError:
        pass

    return HttpResponse("Session Data cleared")





def signup(request):
    if request.method == 'POST':
        uname = request.POST.get('Username')
        pwd = request.POST.get('Password')

        # print("Hashed password is:", make_password(pwd))

        # print(uname, pwd)
        if User.objects.filter(Username=uname).count() > 0:
            return HttpResponse('Username already exists.')
        else:

            form_user = UserForm(request.POST)
            if form_user.is_valid():
                form_user.save()

            return redirect('login')
    else:

        form_user = UserForm()
        return render(request, 'CodeAutoApp/signup.html', {'form_user': form_user})


def login(request):
    if request.method == 'POST':

        # userId= request.POST.get('id')
        uname = request.POST.get('uname')
        pwd = request.POST.get('pwd')

        check_user = User.objects.filter(Username=uname, Password=pwd)
        if check_user:
            request.session['userName'] = uname


            # getting the userId from record
            field_name = 'id'
            obj_user = check_user.first()
            field_object = User._meta.get_field(field_name)
            field_value_userId = field_object.value_from_object(obj_user)

            request.session['userId'] = field_value_userId;  # assign to session

            # create account for sms and runtime user
            obj = Text_Account.objects.filter(userId_id=field_value_userId)
            if obj.count() > 0:
                f = Text_Account(Amount="0", userId_id=field_value_userId)

            else:
                f = Text_Account(Amount="0", userId_id=field_value_userId)
                f.save()

            obj = Runtime_Account.objects.filter(userId_id=field_value_userId)
            if obj.count() > 0:
                f = Runtime_Account(Amount="0", userId_id=field_value_userId)

            else:
                f = Runtime_Account(Amount="0", userId_id=field_value_userId)
                f.save()

            return redirect('home')
        else:
            return HttpResponse('Please enter valid Username or Password.')

    return render(request, 'CodeAutoApp/login.html')


def logout(request):
    try:
        del request.session['userName']
        del request.session['userId']
    except:
        return redirect('home')
    return redirect('home')


def save_session_data(request):
    # set new data
    request.session['user_id'] = 20
    request.session['team'] = 'Barcelona'
    return HttpResponse("Session Data Saved")


def runScript_php(request):
    # lets get account balance

    charge_run = 3;
    field_name = 'Amount'
    obj_account = Runtime_Account.objects.filter(userId_id=request.session['userId'])

    if obj_account.count() > 0:
        obj_account = obj_account.first()
        field_object = Runtime_Account._meta.get_field(field_name)
        field_value_account = field_object.value_from_object(obj_account)

        result = float(field_value_account) - charge_run
        if result > -1:
            field_script = 'Script'
            field_userId = 'UserId_id'
            field_pause = 'Paused'
            field_startDate = 'StartDate'
            field_endDate = 'EndDate'
            RecurrentDate = 'RecurrentDate'
            obj_script = ScriptJob.objects.filter(RecurrentType_id=1, Script_Job_Type_id=2)
            obj_script = obj_script.first()
            field_object = ScriptJob._meta.get_field(field_script)
            field_object1 = ScriptJob._meta.get_field(field_userId)
            field_object2 = ScriptJob._meta.get_field(field_pause)
            field_object3 = ScriptJob._meta.get_field(field_startDate)
            field_object4 = ScriptJob._meta.get_field(field_endDate)
            field_object5 = ScriptJob._meta.get_field(RecurrentDate)

            field_value_script = field_object.value_from_object(obj_script)
            field_value_userId = field_object1.value_from_object(obj_script)
            field_value_paused = field_object2.value_from_object(obj_script)
            field_value_startdate = field_object3.value_from_object(obj_script)
            field_value_endDate = field_object4.value_from_object(obj_script)
            field_value_recurrentDate = field_object5.value_from_object(obj_script)

            runPHP(field_value_script)

            t = Runtime_Account.objects.get(userId_id=field_value_userId)
            t.Amount = result  # change field
            t.save()  # this will update only

    return redirect('home')


def runPHP(scriptVal):
    import string
    import random  # define the random module
    import sys
    # Here we generate 10 random string but for scripts in data base will be concat with id
    S = 10  # number of characters in the string.
    ran = ''.join(random.choices(string.ascii_uppercase + string.digits, k=S))
    ran1 = ''.join(random.choices(string.ascii_uppercase + string.digits, k=S))

    fileName = str(ran1) + str(ran) + ".php"

    if scriptVal[0:5] == "<?php":
        getCode = scriptVal
    else:
        getCode = "<?php " + scriptVal + " ?>"

    fileDirectory = "C:\\Users\\Rex\\PycharmProjects\\pythonProject\\Demoproject\\DemoApp\\php_scripts\\"

    # We first save script to file below
    text_file = open(fileDirectory + fileName, "w")
    text_file.write(getCode)
    text_file.close()

    # here , we run for output
    proc = subprocess.Popen("php " + fileDirectory + fileName, shell=True,
                            stdout=subprocess.PIPE)
    script_response = proc.stdout.read()
    run_result_php = script_response.decode('UTF-8')

    print(run_result_php)

    # Here, we delete the file
    os.remove(fileDirectory + fileName)


def runPyhon(scriptVal, userId):
    import string
    import random  # define the random module
    import sys

    # Here we generate 10 random string but for scripts in data base will be concat with id
    S = 10  # number of characters in the string.
    ran = ''.join(random.choices(string.ascii_uppercase + string.digits, k=S))

    fileName = str(userId) + str(ran) + ".py"

    getCode = scriptVal

    fileDirectory = "C:\\Users\\Rex\\PycharmProjects\\pythonProject\\Demoproject\\DemoApp\\python_scripts\\"

    # We first save script to file below
    text_file = open(fileDirectory + fileName, "w")
    text_file.write(getCode)
    text_file.close()

    old_stdout = sys.stdout
    new_stdout = io.StringIO()
    sys.stdout = new_stdout

    # print("Hello World")

    # print("Hello Universe")

    # try:
    #    exec(open(fileDirectory + fileName).read())
    # except(SyntaxError):
    #    run_result_python ="SyntaxError"

    try:
        exec(open(fileDirectory + fileName).read())

        output = new_stdout.getvalue()

        sys.stdout = old_stdout

        # print(output)

        run_result_python = output
    except NameError:
        run_result_python = "SyntaxError"

    # Here, we delete the file
    os.remove(fileDirectory + fileName)


def configuration_createUserType():
    # here, we create the user account type
    objs = UserType.objects.filter(Name="Individual")
    if objs.count() > 0:
        a = UserType(Name="Individual")

    else:
        a = UserType(Name="Individual")
        a.save()

    objs = UserType.objects.filter(Name="Corporate")
    if objs.count() > 0:
        a = UserType(Name="Corporate")

    else:
        a = UserType(Name="Corporate")
        a.save()


def configuration_createTestUser(request):


    objs = User.objects.filter(Username__contains=Username, mobile=mobile)
    if objs.count() > 0:
        print('')

    else:

        field_name = 'id'
        obj_userType = UserType.objects.filter(Name__contains="Individual")
        obj_test_user = obj_userType.first()
        field_object_UT = UserType._meta.get_field(field_name)
        field_value_userType = field_object_UT.value_from_object(obj_test_user)

        # create the test account
        b = User(FirstName=FirstName, LastName=LastName, mobile=mobile
                 , Email=Email, Username=Username, Password=Password, UserType_id=field_value_userType)
        b.save()

    #we save test user to session
    check_user = User.objects.filter(Username__contains=Username, mobile=mobile)
    field_name = 'id'
    obj_user = check_user.first()
    field_object = User._meta.get_field(field_name)
    field_value_userId = field_object.value_from_object(obj_user)

    # we check if user has login
    if 'userName' in request.session:
        print('session exist')

        '''
        try:
            del request.session['userName']
            del request.session['userId']
        except KeyError:
            pass
        '''

    else:
        print('session does not exist')
        request.session['userName'] = Username
        request.session['userId'] = field_value_userId;  # assign to session


def configuration_createTestFinancialAccount():
    field_name = 'id'
    # get the id from the test account
    obj_test_user = User.objects.filter(Username__contains=Username, mobile=mobile)
    obj_test_user = obj_test_user.first()
    field_object = User._meta.get_field(field_name)
    field_value_userId = field_object.value_from_object(obj_test_user)

    obj = Text_Account.objects.filter(userId_id=field_value_userId)
    if obj.count() > 0:
        f = Text_Account(Amount="0", userId_id=field_value_userId)

    else:
        f = Text_Account(Amount="0", userId_id=field_value_userId)
        f.save()

    # creating for runtime
    obj = Runtime_Account.objects.filter(userId_id=field_value_userId)
    if obj.count() > 0:
        f = Runtime_Account(Amount="0", userId_id=field_value_userId)

    else:
        f = Runtime_Account(Amount="0", userId_id=field_value_userId)
        f.save()

    return field_value_userId

def configuration_createScriptJobType():
    # here, we create the user account type
    objs = ScriptJobType.objects.filter(Name=job_python)
    if objs.count() > 0:
        a = ScriptJobType(Name=job_python)

    else:
        a = ScriptJobType(Name=job_python)
        a.save()

    objs = ScriptJobType.objects.filter(Name=job_php)
    if objs.count() > 0:
        a = ScriptJobType(Name=job_php)

    else:
        a = ScriptJobType(Name=job_php)
        a.save()

def configuration_createRecurrentType():

    objs = RecurrentType.objects.filter(Name=manualSet)
    if objs.count() > 0:
        a = RecurrentType(Name=manualSet)

    else:
        a = RecurrentType(Name=manualSet)
        a.save()

    objs = RecurrentType.objects.filter(Name=everyMinute)
    if objs.count() > 0:
        a = RecurrentType(Name=everyMinute)

    else:
        a = RecurrentType(Name=everyMinute)
        a.save()

    objs = RecurrentType.objects.filter(Name=everyHour)
    if objs.count() > 0:
        a = RecurrentType(Name=everyHour)

    else:
        a = RecurrentType(Name=everyHour)
        a.save()


# Create your views here.
def home(request, id=0):
    se_date = date(2013, 3, 15)
    today = date.today()

    if se_date < today:
        print('greater')
    else:
        print('less')

    configuration_createUserType()  # creating user type
    configuration_createTestUser(request)  # we creat test user account in db
    configuration_createTestFinancialAccount() # we create financial account
    configuration_createScriptJobType() # we create script job type
    configuration_createRecurrentType()# we create recurrent job types

    #print(request.session['userId'])

    # we check if user has login
    if 'userName' in request.session:

        # assigning parameters to configure test view
        field_value_userId = request.session['userId']
        logInStatus = "yes"
        user_test = ""
        print('yes!')

    else:

        logInStatus = "no"
        user_test = "Test"
        print('No!')





    if request.method == "GET":

        form = EmployeeForm()

        return render(request, "CodeAutoApp/homePage.html",
                     {'form': form, "employee_list": Employee.objects.all()})  # this is to pass the list data as well

        # if id == 0:
        # form = EmployeeForm(requests.post())
        # else:
        # employee = Employee.objects.get(pk=id)
        # form = EmployeeForm(requests.post(), instance=employee)

    '''
    else:

        form = EmployeeForm()

        return render(request, "CodeAutoApp/jobs_forms.html",  # final return value
                      {'form': form,
                       "employee_list": Employee.objects.all()})
    '''

def smsJob(request):
    # we check if user has login
    if 'userName' in request.session:

        # assigning parameters to configure test view
        field_value_userId = request.session['userId']
        logInStatus = "yes"
        user_test = ""
        print('yes!')

    else:

        logInStatus = "no"
        user_test = "Test"
        print('No!')

    if request.method == "GET":

        dataList = {"loggedIn": logInStatus, "userId": field_value_userId}

        run_result_sms = ''

        # filtered list
        SMS_list = SMSJob.objects.filter(UserId_id=field_value_userId)

        form_sms = SMSJobForm(dataList)

        return render(request, 'CodeAutoApp/sms_job.html', {'form_sms': form_sms, 'run_result_sms': run_result_sms,
                                                        "SMSJob_list": SMS_list})


    else:
        # for post jobs
        dataList = {"loggedIn": logInStatus, "userId": field_value_userId,
                    "scriptJobType_python": request.session['scriptJobType_python'],
                    "scriptJobType_php": request.session['scriptJobType_php'],
                    "data_sms": request.POST.get("message"),
                    "data_email": request.POST.get("email"),
                    "data_script": request.POST.get("Script"),
                    "data_script_php": request.POST.get("Script")}

        obj = request.POST.copy()

        run_result_sms = ''

        # getting the id of scryp job type
        field_name = 'id'

        field_object = ScriptJobType._meta.get_field(field_name)  # getting field object with field name

        # filtered list
        SMS_list = SMSJob.objects.filter(UserId_id=field_value_userId)


        dataList = {"loggedIn": logInStatus, "userId": field_value_userId}

        SMSMessages = request.POST.get("message")

        if request.POST.get("action") == 'run_sms':  # run the job

            # ploads = {'things': 2, 'total': 25}
            # r = requests.get('https://httpbin.org/get', params=ploads)
            ploads = '';
            r = requests.get(
                'https://api.wirepick.com/httpsms/send?client=TTH101010&password=Keep@123$&phone=233544875339&text=Hello Lindy',
                params=ploads)
            print(r.text)
            print(r.url)

            ''' below is for post data to appi
            pload = {'username': 'Olivia', 'password': '123'}
            r = requests.post('https://httpbin.org/post', data=pload)
            print(r.text)
            '''

            run_result_sms = 'run1'


        else:  # Save the Job

            run_result_sms = 'save1'


            if request.session['userName'] =='testUserName':
                return render(request, "CodeAutoApp/login.html")


            else:

                form_sms = SMSJob(dataList, obj)
                if form_sms.is_valid():
                    form_sms.save()

        # this is to pre-
        initial_message = {
            "message": SMSMessages,
            "UserId": field_value_userId
        }

        form_sms = SMSJobForm(dataList, initial=initial_message)

        return render(request, "CodeAutoApp/sms_job.html",  # final return value
                      {'form_sms': form_sms, 'run_result_sms': run_result_sms, "SMSJob_list": SMS_list})


def pythonJob(request):
    # we check if user has login
    if request.session['userName'] =='testUserName':
        field_value_userId = request.session['userId']
        logInStatus = "no"
        user_test = "Test"
        print('No!')

    else:
        # assigning parameters to configure test view
        field_value_userId = request.session['userId']
        logInStatus = "yes"
        user_test = ""
        print('yes!')



    if request.method == "GET":

        request.session['scriptJobType_python'] = "Python";
        request.session['scriptJobType_php'] = "PHP";



        dataList = {"loggedIn": logInStatus, "userId": field_value_userId,
                    "scriptJobType_python": request.session['scriptJobType_python'],
                    "scriptJobType_php": request.session['scriptJobType_php'],
                    "data_sms": request.POST.get("message"),
                    "data_email": request.POST.get("email"),
                    "data_script": request.POST.get("Script"),
                    "data_script_php": request.POST.get("Script")}


        run_result_python = ''


        # getting the id of scrypt  job type. this is to filter the python list and php list in my list
        field_name = 'id'

        obj_py = ScriptJobType.objects.filter(Name__icontains=request.session['scriptJobType_python'])
        obj_py = obj_py.first()
        field_object = ScriptJobType._meta.get_field(field_name)  # getting field object with field name
        field_value_python = field_object.value_from_object(obj_py)


        # filtered list
        ScriptJob_list = ScriptJob.objects.filter(Script_Job_Type=field_value_python, UserId_id=field_value_userId)

        # this is to pre- set values for script job type foreign key
        initial_dict_pyt = {
            "UserId": field_value_userId,
            "Script_Job_Type": field_value_python,
        }


        form_script = ScriptJobForm(dataList,
                                    initial=initial_dict_pyt)  # we are passing the user id in session to receive on form

        return render(request, "CodeAutoApp/python_job.html",
                      {'form_script': form_script, 'run_result_python': run_result_python,
                       "ScriptJob_list": ScriptJob_list})  # this is to pass the list data as well

    else:

        dataList = {"loggedIn": logInStatus, "userId": field_value_userId,
                    "scriptJobType_python": request.session['scriptJobType_python'],
                    "scriptJobType_php": request.session['scriptJobType_php'],
                    "data_sms": request.POST.get("message"),
                    "data_email": request.POST.get("email"),
                    "data_script": request.POST.get("Script"),
                    "data_script_php": request.POST.get("Script")}

        obj = request.POST.copy()

        run_result_python = ''

        # getting the id of scryp job type
        field_name = 'id'

        obj_py = ScriptJobType.objects.filter(Name__contains=request.session['scriptJobType_python'])
        obj_py = obj_py.first()
        field_object = ScriptJobType._meta.get_field(field_name)  # getting field object with field name
        field_value_python = field_object.value_from_object(obj_py)

        ScriptJob_list = ScriptJob.objects.filter(Script_Job_Type=field_value_python, UserId_id=field_value_userId)

        if request.POST.get("action") == 'run_python':  # run the job

            import string
            import random  # define the random module
            import sys

            # Here we generate 10 random string but for scripts in data base will be concat with id
            S = 10  # number of characters in the string.
            ran = ''.join(random.choices(string.ascii_uppercase + string.digits, k=S))

            fileName = str(field_value_userId) + str(ran) + ".py"

            getCode = request.POST.get("Script")

            if getCode[:1].isdigit():
                run_result_python = "SyntaxError"
            else:

                fileDirectory = "C:\\Users\\Rex\\PycharmProjects\\CodeAuto\\CodeAuto\\CodeAutoApp\\python_scripts\\"

                # We first save script to file below
                text_file = open(fileDirectory + fileName, "w")
                text_file.write(getCode)
                text_file.close()

                old_stdout = sys.stdout
                new_stdout = io.StringIO()
                sys.stdout = new_stdout

                # print("Hello World")

                # print("Hello Universe")

                # try:
                #    exec(open(fileDirectory + fileName).read())
                # except(SyntaxError):
                #    run_result_python ="SyntaxError"

                try:
                    exec(open(fileDirectory + fileName).read())

                    output = new_stdout.getvalue()

                    sys.stdout = old_stdout

                    # print(output)

                    run_result_python = output
                except NameError:
                    run_result_python = "SyntaxError"

                # Here, we delete the file
                os.remove(fileDirectory + fileName)

        else:  # Save the Job

            if request.session['userName'] =='testUserName':
                form_script_python = ScriptJobForm(dataList, obj)
                if form_script_python.is_valid():
                    form_script_python.save()

            else:

                return render(request, "CodeAutoApp/login.html")

    ScriptType_py = request.POST.get("Script")

    initial_dict_pyt = {
        "Script": ScriptType_py,
        "UserId": field_value_userId,
        "Script_Job_Type": field_value_python,
    }

    form_script = ScriptJobForm(dataList, initial=initial_dict_pyt)

    return render(request, "CodeAutoApp/python_job.html",
                  {'form_script': form_script, 'run_result_python': run_result_python,
                   "ScriptJob_list": ScriptJob_list})  # this is to pass the list data as well


def phpJobs(request):

    print(request.POST)

    if request.session['userName'] =='testUserName':
        field_value_userId = request.session['userId']
        logInStatus = "no"
        user_test = "Test"
        print('No!')

    else:
        # assigning parameters to configure test view
        field_value_userId = request.session['userId']
        logInStatus = "yes"
        user_test = ""
        print('yes!')

    if request.method == "GET":
        request.session['scriptJobType_python'] = "Python";
        request.session['scriptJobType_php'] = "PHP";

        dataList = {"loggedIn": logInStatus, "userId": field_value_userId,
                    "scriptJobType_python": request.session['scriptJobType_python'],
                    "scriptJobType_php": request.session['scriptJobType_php'],
                    "data_sms": request.POST.get("message"),
                    "data_email": request.POST.get("email"),
                    "data_script": request.POST.get("Script"),
                    "data_script_php": request.POST.get("Script")}

        run_result_php = ''

        # getting the id of scrypt  job type. this is to filter the python list and php list in my list
        field_name = 'id'

        obj_php = ScriptJobType.objects.filter(Name__icontains=request.session['scriptJobType_php'])
        obj_php = obj_php.first()
        field_object = ScriptJobType._meta.get_field(field_name)  # getting field object with field name
        field_value_php = field_object.value_from_object(obj_php)

        ScriptJob_list_php = ScriptJob.objects.filter(Script_Job_Type=field_value_php, UserId_id=field_value_userId)

        # this is to pre- set values for script job type foreign key
        initial_dict_php = {
            "UserId": field_value_userId,
            "Script_Job_Type": field_value_php,
        }

        form_script_php = ScriptJobForm_PHP(dataList,
                                            initial=initial_dict_php)

        return render(request, 'CodeAutoApp/php_job.html',
                      {'form_script_php': form_script_php, 'run_result_php': run_result_php,
                       "ScriptJob_list_php": ScriptJob_list_php})



    else:

        dataList = {"loggedIn": logInStatus, "userId": field_value_userId,
                    "scriptJobType_python": request.session['scriptJobType_python'],
                    "scriptJobType_php": request.session['scriptJobType_php'],
                    "data_sms": request.POST.get("message"),
                    "data_email": request.POST.get("email"),
                    "data_script": request.POST.get("Script"),
                    "data_script_php": request.POST.get("Script")}

        obj = request.POST.copy()

        run_result_php = ''

        # getting the id of scryp job type
        field_name = 'id'

        obj_php = ScriptJobType.objects.filter(Name__contains=request.session['scriptJobType_php'])
        obj_php = obj_php.first()

        field_object = ScriptJobType._meta.get_field(field_name)  # getting field object with field name
        field_value_php = field_object.value_from_object(obj_php)

        # filtered list
        ScriptJob_list_php = ScriptJob.objects.filter(Script_Job_Type=field_value_php, UserId_id=field_value_userId)



        if request.POST.get("action") == 'run_php' or request.POST.get(
                "action") == 'save_php':

            ScriptType_php = request.POST.get("Script")

        else:
            ScriptType_php = ''

        if request.POST.get("action") == 'run_php':  # run the job

            import string
            import random  # define the random module

            # Here we generate 10 random string but for scripts in data base will be concat with id
            S = 10  # number of characters in the string.
            ran = ''.join(random.choices(string.ascii_uppercase + string.digits, k=S))

            fileName = str(field_value_userId) + str(ran) + ".php"

            if request.POST.get("Script")[0:5] == "<?php":
                getCode = request.POST.get("Script")
            else:
               # getCode = "<?php " + request.POST.get("Script") + " ?>"
               getCode = request.POST.get("Script")

            fileDirectory = "C:\\Users\\Rex\\PycharmProjects\\CodeAuto\\CodeAuto\\CodeAutoApp\\php_scripts\\"

            # We first save script to file below
            text_file = open(fileDirectory + fileName, "w")
            text_file.write(getCode)
            text_file.close()




            # here , we run for output
            proc = subprocess.Popen("php " + fileDirectory + fileName, shell=True,
                                    stdout=subprocess.PIPE)
            script_response = proc.stdout.read()
            run_result_php = script_response.decode('UTF-8')
            #run_result_php = 'echo"<h2>PHP is Fun!</h2>";'


            
            # if run_result_python[0:7] == 'Warning':
            #   run_result_php="SyntaxError"

            if "Warning" in run_result_php:
                run_result_php = "SyntaxError"

            # Here, we delete the file
            os.remove(fileDirectory + fileName)



        else:  # Save the Job

            if request.session['userName'] !='testUserName':

                form_script_php = ScriptJobForm_PHP(dataList, obj)
                if form_script_php.is_valid():
                    form_script_php.save()

            else:

                return render(request, "DemoApp/login.html")

        initial_dict_php = {
            "Script": ScriptType_php,
            "UserId": field_value_userId,
            "Script_Job_Type": field_value_php,
        }

        form_script_php = ScriptJobForm_PHP(dataList, initial=initial_dict_php)

        #run_result_php = 'echo "<h2>PHP is Fun!</h2>";'
    return render(request, 'CodeAutoApp/php_job.html',
                  {'form_script_php': form_script_php, 'run_result_php': run_result_php,
                   "ScriptJob_list_php": ScriptJob_list_php})


def employee_list(request):
    # we will write matplot codes here
    plt.plot(range(10))
    fig = plt.gcf()
    # convert graph into dtring buffer and then we convert 64 bit code into image
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = urllib.parse.quote(string)

    context = {"employee_list": Employee.objects.all()}
    return render(request, 'DemoApp/employee_list.html', {"employee_list": Employee.objects.all(), 'data': uri})


def buyRunCredit(request, id=0):


    print(request.POST)

    return render(request, "CodeAutoApp/buy_run_credit.html",
                     { "employee_list": Employee.objects.all()})  # this is to pass the list data as well


def buySMSCredit(request, id=0):
    return render(request, "CodeAutoApp/buy_sms_credit.html",
                  {"employee_list": Employee.objects.all()})  # this is to pass the list data as well


def automations(request, id=0):
    return render(request, "CodeAutoApp/automations.html")  # this is to pass the list data as well
def centers(request, id=0):
    return render(request, "CodeAutoApp/centers.html")  # this is to pass the list data as well
def branches(request, id=0):

    return render(request, "CodeAutoApp/branches.html")  # this is to pass the list data as well
def about(request, id=0):
    return render(request, "CodeAutoApp/about.html")  # this is to pass the list data as well

def contact(request, id=0):
    return render(request, "CodeAutoApp/contacts.html")  # this is to pass the list data as well
def howItWorks(request, id=0):
    return render(request, "CodeAutoApp/howItWorks.html")  # this is to pass the list data as well
def terms(request, id=0):
    return render(request, "CodeAutoApp/terms.html")  # this is to pass the list data as well
def policy(request, id=0):

    return render(request, "CodeAutoApp/policy.html")  # this is to pass the list data as well
def moneyback(request, id=0):
    return render(request, "CodeAutoApp/moneyback.html")  # this is to pass the list data as well





def delete(request, id):
    employee = Employee.objects.get(pk=id)
    employee.delete()
    return


def data_visuals(request):
    from pandas import DataFrame
    import pandas as pd
    import numpy as np
    import seaborn as sn

    data1 = {'Country': ['US', 'CA', 'GER', 'UK', 'FR'],
             'GDP_Per_Capita': [45000, 42000, 52000, 49000, 47000]
             }
    df1 = DataFrame(data1, columns=['Country', 'GDP_Per_Capita'])

    data2 = {'Year': [1920, 1930, 1940, 1950, 1960, 1970, 1980, 1990, 2000, 2010],
             'Unemployment_Rate': [9.8, 12, 8, 7.2, 6.9, 7, 6.5, 6.2, 5.5, 6.3]
             }
    df2 = DataFrame(data2, columns=['Year', 'Unemployment_Rate'])

    data3 = {'Interest_Rate': [5, 5.5, 6, 5.5, 5.25, 6.5, 7, 8, 7.5, 8.5],
             'Stock_Index_Price': [1500, 1520, 1525, 1523, 1515, 1540, 1545, 1560, 1555, 1565]
             }
    df3 = DataFrame(data3, columns=['Interest_Rate', 'Stock_Index_Price'])

    figure1 = plt.Figure(figsize=(6, 5), dpi=100)
    ax1 = figure1.add_subplot(111)
    df1.plot(kind='bar', legend=True, ax=ax1)
    ax1.set_title('Country Vs. GDP Per Capita')
    ax1.set_xlabel('Rex')
    # convert graph into dtring buffer and then we convert 64 bit code into image
    buf = io.BytesIO()
    figure1.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = urllib.parse.quote(string)

    figure2 = plt.Figure(figsize=(5, 4), dpi=100)
    ax2 = figure2.add_subplot(111)
    df2 = df2[['Year', 'Unemployment_Rate']].groupby('Year').sum()
    df2.plot(kind='line', legend=True, ax=ax2, color='r', marker='o', fontsize=10)
    ax2.set_title('Year Vs. Unemployment Rate')
    # convert graph into dtring buffer and then we convert 64 bit code into image
    buf = io.BytesIO()
    figure2.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri1 = urllib.parse.quote(string)

    figure3 = plt.Figure(figsize=(5, 4), dpi=100)
    ax3 = figure3.add_subplot(111)
    ax3.scatter(df3['Interest_Rate'], df3['Stock_Index_Price'], color='g')
    ax3.legend(['Stock_Index_Price'])
    ax3.set_xlabel('Interest Rate')
    ax3.set_title('Interest Rate Vs. Stock Index Price')
    # convert graph into dtring buffer and then we convert 64 bit code into image
    buf = io.BytesIO()
    figure3.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri2 = urllib.parse.quote(string)


    #Patient_list = Patient.objects.using('healthpro').filter(firstmonthid='MTH202108')
    # Patient_list = Patient.objects.using('healthpro').filter(firstyearid='YRS2021')
    # df = pd.DataFrame(list(Patient_list.values("firstname")))
    #df = pd.DataFrame(list(Patient_list.values()))
    df= pd.DataFrame()

    df7 = df[['firstmonthid', 'age']].groupby('firstmonthid').count()
    figure7 = plt.Figure(figsize=(6, 5), dpi=100)
    ax7 = figure7.add_subplot(111)
    df7.plot(kind='bar', legend=True, ax=ax7)
    ax7.set_title('Gender count')
    ax7.set_xlabel('Gender')
    for i, v in enumerate(df['age']):
        ax7.text(v + 3, i + .25, str(v), color='blue', fontweight='bold')
    # convert graph into string buffer and then we convert 64 bit code into image
    buf = io.BytesIO()
    figure7.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri7 = urllib.parse.quote(string)

    x = [u'INFO', u'CUISINE', u'TYPE_OF_PLACE', u'DRINK', u'PLACE', u'MEAL_TIME', u'DISH', u'NEIGHBOURHOOD']
    y = [160, 167, 137, 18, 120, 36, 155, 130]

    fig, ax = plt.subplots()
    width = 0.75  # the width of the bars
    ind = np.arange(len(y))  # the x locations for the groups
    ax.barh(ind, y, width, color="blue")
    ax.set_yticks(ind + width / 2)
    ax.set_yticklabels(x, minor=False)
    plt.title('title')
    plt.xlabel('x')
    plt.ylabel('y')
    for i, v in enumerate(y):
        ax.text(v + 3, i + .25, str(v), color='blue', fontweight='bold')

    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri3 = urllib.parse.quote(string)

    # below is a section for naive_bayes

    from sklearn import preprocessing
    from sklearn.naive_bayes import GaussianNB

    weather = ['Sunny', 'Sunny', 'Overcast', 'Rainy', 'Rainy', 'Rainy', 'Overcast', 'Sunny', 'Sunny',
               'Rainy', 'Sunny', 'Overcast', 'Overcast', 'Rainy']
    temp = ['Hot', 'Hot', 'Hot', 'Mild', 'Cool', 'Cool', 'Cool', 'Mild', 'Cool', 'Mild', 'Mild', 'Mild', 'Hot', 'Mild']

    play = ['No', 'No', 'Yes', 'Yes', 'Yes', 'No', 'Yes', 'No', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'No']

    # creating labelEncoder
    le = preprocessing.LabelEncoder()
    # Converting string labels into numbers.
    weather_encoded = le.fit_transform(weather)

    print("weather: ", weather_encoded)

    temp_encoded = le.fit_transform(temp)

    label = le.fit_transform(play)

    print("Temp:", temp_encoded)
    print("label:", label)

    features = zip(weather_encoded, temp_encoded)
    features_l = list(features)
    print(features_l)

    # Create a Gaussian Classifier
    model = GaussianNB()

    # Train the model using the training sets
    model.fit(features_l, label)

    # Predict Output
    predicted = model.predict([[0, 2]])  # 0:Overcast, 2:Mild
    print("Predicted Value:", predicted)

    predicted_string = le.inverse_transform(predicted)
    print("Predicted string:", predicted_string)

    # Multinomial Naive Bayes. Classification for multiple labels or independent variable(y)
    from sklearn import datasets
    from sklearn.model_selection import train_test_split
    from sklearn.naive_bayes import GaussianNB
    from sklearn import metrics

    wine = datasets.load_wine()

    # print("Features: ", wine.feature_names) # print the names of the 13 features
    # print("Labels: ", wine.target_names) # print the label type of wine(class_0, class_1, class_2)
    # print(wine.data.shape) # print data(feature)shape
    # print(wine.data[0:5]) # print the wine data features (top 5 records)
    # print (wine.target)  # print the wine labels (0:Class_0, 1:class_2, 2:class_2)

    # Split dataset into training set and test set
    X_train, X_test, y_train, y_test = train_test_split(wine.data, wine.target, test_size=0.3,
                                                        random_state=109)  # 70% training and 30% test
    # Create a Gaussian Classifier
    gnb = GaussianNB()

    # Train the model using the training sets
    gnb.fit(X_train, y_train)

    # Predict the response for test dataset
    y_pred = gnb.predict(X_test)

    # Model Accuracy, how often is the classifier correct?
    print("Accuracy:", metrics.accuracy_score(y_test, y_pred))
    print(y_pred)

    # Anova testing . categorical variable that has most impact on age
    # df_anova = df[['genderid','age']]
    # grouped_anova=df_anova.groupby(['genderid'])

    # correlation
    # sn.regplot(x="", y="", data=df)
    # plt.ylim(0,)

    # sn.set_theme(style="darkgrid")
    # titanic = sn.load_dataset(df[['firstmonthid']])
    # ax = sn.countplot(x="class", data=titanic)

    '''


    #pivoting a table
    df_test= df[["genderid","religionid","age"]]
    df_grp=df_test.groupby(["genderid","religionid"],as_index=False).mean()
    df_pivot=df_grp.pivot(index='genderid',columns='religionid')
    #print(df_pivot)


    #data binning
    bins=np.linspace(min(df['age']),max(df['age']),4)
    group_names=["young","mid-age","old"]
    df["age-binned"]=pd.cut(df["age"],bins,labels=group_names,include_lowest=True)
    #print(df["age-binned"])

    #Tranforming categorical variables to dummy variables
    dum = pd.get_dummies(df['genderid'])
    print(dum)



    '''

    return render(request, "DemoApp/data_visualizations.html",  # final return value
                  {'data': uri, 'data1': uri1, 'data2': uri2, 'data3': uri3, 'data7': uri7,
                   'Patient_list': Patient_list})


'''
def hi(request):
    output = ""
    # Initialize the form. At this point you have an unbound/invalid form
    myform = command_form()  # better write it as CommandForm

    if request.method == "POST":
        myform = command_form(request.POST)
        if myform.is_valid():
            # execute_command variable, should now contain the command typed by the user in the text box
            execute_command = myform.cleaned_data['command']
            try:
                # If the return code is non-zero, CalledProcessError will be raised
                output = sp.check_output(execute_command, shell=True)
            except sp.CalledProcessError:
                exit_code, error_msg = output.returncode, output.output

    return render(request, 'DemoApp/homePage.html', locals())

'''

'''
# we will write matplot codes here
plt.plot(range(10))
fig = plt.gcf()
# convert graph into dtring buffer and then we convert 64 bit code into image
buf = io.BytesIO()
fig.savefig(buf, format='png')
buf.seek(0)
string = base64.b64encode(buf.read())
uri = urllib.parse.quote(string)



'''
