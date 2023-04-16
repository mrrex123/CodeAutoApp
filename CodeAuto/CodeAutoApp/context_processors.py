from . import views
from .models import Runtime_Account
from .models import Text_Account
from .forms import runAccountForm
from .forms import smsAccountForm
from .models import User



def add_variable_to_context(request,):
    if 'userName' in request.session:
        if  request.session['userName'] =='testUserName':
            return {
                #'current_user': request.session['userName'],
                #'runningAccount': getRunAccountForm(request.session['userName'], request.session['userId']),
                #'smsAccount': getSMSAccountForm(request.session['userName'], request.session['userId'])
            }
        else:
            return {
                 'current_user': request.session['userName'],
                 'runningAccount': getRunAccountForm(request.session['userName'], request.session['userId']),
                 'smsAccount': getSMSAccountForm(request.session['userName'], request.session['userId'])
        }

    else:
        return {
        'runningAccount': getRunAccountForm("",""),
        'smsAccount': getSMSAccountForm("", "")
        }


def getRunAccountForm(userName,field_value_userId):
    # we check if user has login
        if len(userName)>0:
           field_value_userId
        else:
           field_value_userId = configuration_createTestFinancialAccount()

        # getting the value in the field of an object
        field_name = 'Amount'
        obj = Runtime_Account.objects.filter(userId_id=field_value_userId)
        obj = obj.first()
        field_object_run = Runtime_Account._meta.get_field(field_name)
        field_value_run = field_object_run.value_from_object(obj)

        field_name_run = 'Amount'
        obj = Text_Account.objects.filter(userId_id=field_value_userId)
        obj = obj.first()
        field_object_sms = Text_Account._meta.get_field(field_name_run)
        field_value_sms = field_object_sms.value_from_object(obj)

        initial_dict_run = {
            "Amount": field_value_run,
        }

        initial_dict_sms = {
            "Amount": field_value_sms,
        }

        form_runTime = runAccountForm(initial=initial_dict_run)
        form_smsTime = smsAccountForm(initial=initial_dict_sms)

        return form_runTime


def getSMSAccountForm(userName,field_value_userId):
    # we check if user has login
        if len(userName)>0:
           field_value_userId
        else:
           field_value_userId = configuration_createTestFinancialAccount()

        # getting the value in the field of an object
        field_name = 'Amount'
        obj = Runtime_Account.objects.filter(userId_id=field_value_userId)
        obj = obj.first()
        field_object_run = Runtime_Account._meta.get_field(field_name)
        field_value_run = field_object_run.value_from_object(obj)

        field_name_run = 'Amount'
        obj = Text_Account.objects.filter(userId_id=field_value_userId)
        obj = obj.first()
        field_object_sms = Text_Account._meta.get_field(field_name_run)
        field_value_sms = field_object_sms.value_from_object(obj)

        initial_dict_run = {
            "Amount": field_value_run,
        }

        initial_dict_sms = {
            "Amount": field_value_sms,
        }

        form_runTime = runAccountForm(initial=initial_dict_run)
        form_smsTime = smsAccountForm(initial=initial_dict_sms)

        return form_smsTime

def configuration_createTestFinancialAccount():
    field_name='id'
    # get the id from the test account
    obj_test_user = User.objects.filter(FirstName__contains="Test", mobile='0000000000')
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