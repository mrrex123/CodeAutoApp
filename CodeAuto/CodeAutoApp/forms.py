from django import forms
from .models import Employee
from .models import Position
from .models import ScriptJob
from .models import ScriptJob_PHP
from .models import SMSJob
from .models import Text_Account
from .models import Runtime_Account

from .models import ScriptJobType
from .models import User

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import datetime



# class command_form(forms.Form):
#  command = forms.CharField(max_length=200)

# class CustomUserChoiceField(forms.ModelChoiceField):
#    def label_from_instance(self, Employee):
#      return Employee.get_full_name()


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        # fields = '__all__' you can use this to pick all model fields at a go
        fields = ('fullname', 'mobile', 'emp_code', 'position')
        labels = {
            'fullname': 'Full Name',
            'emp_code': 'EMP. Code'

        }

    # this function is used to have 'select' for the position dropdown n to process properties of th form
    def __init__(self, *args, **kwargs):
        super(EmployeeForm, self).__init__(*args, **kwargs)
        self.fields['position'].empty_label = "select"
        self.fields['position'].queryset = Position.objects.filter(id=2)
        self.fields['emp_code'].required = False


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'  # you can use this to pick all model fields at a go

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['UserType'].empty_label = "select"


class runAccountForm(forms.ModelForm):
    class Meta:
        model = Runtime_Account
        fields = ('Amount',)
        labels = {
            'Amount': 'Run Time Balance',
        }

    def __init__(self, *args, **kwargs):
        super(runAccountForm, self).__init__(*args, **kwargs)
        self.fields['Amount'].required = False
        self.fields['Amount'].widget.attrs['readonly'] = True


class smsAccountForm(forms.ModelForm):
    class Meta:
        model = Text_Account
        fields = ('Amount',)
        labels = {
            'Amount': 'SMS Balance',
        }

    def __init__(self, *args, **kwargs):
        super(smsAccountForm, self).__init__(*args, **kwargs)
        self.fields['Amount'].required = False
        self.fields['Amount'].widget.attrs['readonly'] = True

BIRTH_YEAR_CHOICES = ['1980', '1981', '1982']
FAVORITE_COLORS_CHOICES = [
    ('blue', 'Blue'),
    ('green', 'Green'),
    ('black', 'Black'),
]
class ScriptJobForm(forms.ModelForm):

    '''
    birth_year = forms.DateField(widget=forms.SelectDateWidget(years=BIRTH_YEAR_CHOICES))
    favorite_colors = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=FAVORITE_COLORS_CHOICES,
    )
   '''

    class Meta:
        model = ScriptJob
        fields = '__all__'  # you can use this to pick all model fields at a go


    def __init__(self, round_list, *args, **kwargs):
        super(ScriptJobForm, self).__init__(*args, **kwargs)
        self.fields['RecurrentType'].empty_label = 'Select'

        self.fields['StartDate']= forms.CharField(widget= forms.TextInput
                           (attrs={'placeholder':'Enter date eg dd/mm/yy'}))

        #self.fields['StartDate']=forms.IntegerField(validators=[validate_even])
        #self.fields['StartDate']  = forms.DateField(widget=forms.SelectDateWidget(years=BIRTH_YEAR_CHOICES))
        #self.fields['StartDate']  = forms.DateField(widget=forms.DateInput(format='%d%m%Y'),
        #input_formats=['%d%m%Y'])

        # queryset_user=User.objects.filter(id= round_list["userId"])
        # self.fields['UserId'].empty_label = queryset_user[0]
        self.fields['UserId'].queryset = User.objects.filter(id=round_list["userId"])

        # queryset=ScriptJobType.objects.filter(Name__icontains=round_list["scriptJobType_python"])
        # self.fields['Script_Job_Type'].empty_label = queryset[0]
        self.fields['Script_Job_Type'].queryset = ScriptJobType.objects.filter(
            Name__icontains=round_list["scriptJobType_python"])

        self.fields['Paused'].widget.attrs['readonly'] = True
        self.fields['Paused'].required = False

def validate_even(value):
    if value % 2 != 0:
        raise ValidationError(
            _('%(value)s is not an even number'),
            params={'value': value},
        )
'''
        if round_list["loggedIn"] == 'no':
            self.fields['RecurrentType'].required = False
            self.fields['RecurrentDate'].required = False
            self.fields['StartDate'].required = False
            self.fields['EndDate'].required = False
            self.fields['UserId'].required = False
            self.fields['Script_Job_Type'].required = False
'''

class ScriptJobForm_PHP(forms.ModelForm):
    class Meta:
        model = ScriptJob
        fields = '__all__'  # you can use this to pick all model fields at a go

    def __init__(self, round_list, *args, **kwargs):
        super(ScriptJobForm_PHP, self).__init__(*args, **kwargs)
        self.fields['RecurrentType'].empty_label = "select"
        self.fields['UserId'].queryset = User.objects.filter(id=round_list["userId"])

        self.fields['Script_Job_Type'].queryset = ScriptJobType.objects.filter(
            Name__icontains=round_list["scriptJobType_php"])

        self.fields['Paused'].widget.attrs['readonly'] = True
        self.fields['Paused'].required = False


        '''
        if round_list["loggedIn"]=='no':
            self.fields['RecurrentType'].required = False
            self.fields['RecurrentDate'].required = False
            self.fields['StartDate'].required = False
            self.fields['EndDate'].required = False
            self.fields['UserId'].required = False
            self.fields['Script_Job_Type'].required = False
        '''

    def clean_field(self):
        data = self.cleaned_data['Script']
        if not data:
            data = 'default value'
            #datetime.date.today()  # Returns 2018-01-15
            #datetime.datetime.now()  # Returns 2018-01-15 09:00
           # raise forms.ValidationError("The date cannot be in the past!")
        return data


    #def clean_date(self):
     #   date = self.cleaned_data['date']
      #  if date < datetime.date.today():
      #      raise forms.ValidationError("The date cannot be in the past!")
      #  return date


class SMSJobForm(forms.ModelForm):
    class Meta:
        model = SMSJob
        fields = '__all__'  # you can use this to pick all model fields at a go

    def __init__(self, round_list, *args, **kwargs):
        super(SMSJobForm, self).__init__(*args, **kwargs)
        self.fields['SenderId'].empty_label = "select"
        self.fields['RecurrentType'].empty_label = "select"

'''
class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = '__all__'  # you can use this to pick all model fields at a go

    def __init__(self, *args, **kwargs):
        super(SMSJobForm, self).__init__(*args, **kwargs)
'''

class DateForm(forms.Form):
    date = forms.DateTimeField(
        input_formats=['%d/%m/%Y %H:%M'],
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control datetimepicker-input',
            'data-target': '#datetimepicker1'
        })
    )
