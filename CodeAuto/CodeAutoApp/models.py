from asyncio import Event

from django.db import models

from django.db import models
import datetime
from django.core.exceptions import ValidationError


# Create your models here.

class Position(models.Model):
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title


class Employee(models.Model):
    fullname = models.CharField(max_length=100)
    emp_code = models.CharField(max_length=3)
    mobile = models.CharField(max_length=15)
    position = models.ForeignKey(Position, on_delete=models.CASCADE)


class UserType(models.Model):
    Name = models.CharField(max_length=100)

    def __str__(self):
        return self.Name


class CorporateAccountType(models.Model):
    Name = models.CharField(max_length=100)


class User(models.Model):
    UserType = models.ForeignKey(UserType, on_delete=models.CASCADE)
    FirstName = models.CharField(max_length=100)
    LastName = models.CharField(max_length=100)
    mobile = models.CharField(max_length=15)
    Email = models.CharField(max_length=100)
    Username = models.CharField(max_length=100)
    Password = models.CharField(max_length=100)

    def __str__(self):
        return self.FirstName + " " + self.LastName


class Text_Account(models.Model):
    Amount = models.CharField(max_length=100)
    userId = models.ForeignKey(User, on_delete=models.CASCADE)


class Runtime_Account(models.Model):
    Amount = models.CharField(max_length=100)
    userId = models.ForeignKey(User, on_delete=models.CASCADE)


class ScriptJobType(models.Model):
    Name = models.CharField(max_length=200)

    def __str__(self):
        return self.Name


class RecurrentType(models.Model):
    Name = models.CharField(max_length=200)

    def __str__(self):
        return self.Name


class ScriptJob(models.Model):
    Script = models.TextField(max_length=2000)
    RecurrentType = models.ForeignKey(RecurrentType, on_delete=models.CASCADE)
    RecurrentDate = models.CharField(max_length=200)
    StartDate = models.CharField(max_length=200)
    EndDate = models.CharField(max_length=200)
    UserId = models.ForeignKey(User, on_delete=models.CASCADE)
    Script_Job_Type = models.ForeignKey(ScriptJobType, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    Paused = models.CharField(max_length=15)





class ScriptJob_PHP(models.Model):
    Script = models.TextField(max_length=2000)
    RecurrentType = models.ForeignKey(RecurrentType, on_delete=models.CASCADE)
    RecurrentDate = models.CharField(max_length=200)
    StartDate = models.CharField(max_length=200)
    EndDate = models.CharField(max_length=200)
    UserId = models.ForeignKey(User, on_delete=models.CASCADE)
    Script_Job_Type = models.ForeignKey(ScriptJobType, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    Paused = models.CharField(max_length=15)




class SenderIds(models.Model):
    Name = models.CharField(max_length=100)

    def __str__(self):
        return self.Name


class SMSJob(models.Model):
    message = models.TextField(max_length=2000)
    SenderId = models.ForeignKey(SenderIds, on_delete=models.CASCADE)
    RecurrentType = models.ForeignKey(RecurrentType, on_delete=models.CASCADE)
    RecurrentDate = models.CharField(max_length=200)
    StartDate = models.CharField(max_length=200)
    EndDate = models.CharField(max_length=200)
    UserId = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    Paused = models.CharField(max_length=15)


#StartDate = models.DateField("StartDate (mm/dd/yyyy)",auto_now_add=False, auto_now=False, blank=True)

class SMSContact(models.Model):
    contact_phone = models.CharField(max_length=100)
    SMS_Job_Id = models.ForeignKey(SMSJob, on_delete=models.CASCADE)


class EmailAddresses(models.Model):
    emails = models.CharField(max_length=100)


class EmailJob(models.Model):
    MessageSubject = models.CharField(max_length=200)
    message = models.TextField(max_length=5000)
    SenderEmailAddress = models.ForeignKey(EmailAddresses, on_delete=models.CASCADE)
    RecurrentType = models.ForeignKey(RecurrentType, on_delete=models.CASCADE)
    RecurrentDate = models.CharField(max_length=200)
    StartDate = models.CharField(max_length=200)
    EndDate = models.CharField(max_length=200)
    UserId = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    Paused = models.CharField(max_length=15)


class EmailContact(models.Model):
    contact_phone = models.CharField(max_length=100)
    Email_Job_Id = models.ForeignKey(EmailJob, on_delete=models.CASCADE)


class Result_Email_Runtime(models.Model):
    Email_Job_Id = models.ForeignKey(EmailJob, on_delete=models.CASCADE)
    ResultOutput = models.CharField(max_length=200)
    UserId = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    Paused = models.CharField(max_length=15)


class Result_SMS_Runtime(models.Model):
    SMS_Job_Id = models.ForeignKey(SMSJob, on_delete=models.CASCADE)
    ResultOutput = models.CharField(max_length=200)
    UserId = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    Paused = models.CharField(max_length=15)


class Result_Script_Runtime(models.Model):
    Script_Job_Id = models.ForeignKey(ScriptJob, on_delete=models.CASCADE)
    Script_Job_Type = models.ForeignKey(ScriptJobType, on_delete=models.CASCADE)
    ResultOutput = models.CharField(max_length=200)
    UserId = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    Paused = models.CharField(max_length=15)


class InvoiceType(models.Model):
    name = models.CharField(max_length=200)


class Invoices(models.Model):
    Invoice_Type_Id = models.ForeignKey(InvoiceType, on_delete=models.CASCADE)
    userId = models.ForeignKey(User, on_delete=models.CASCADE)
    aapf_txn_amt = models.CharField(max_length=200)
    aapf_txn_clientRspRedirectURL = models.CharField(max_length=200)
    aapf_txn_clientTxnWH = models.CharField(max_length=200)
    aapf_txn_cref = models.CharField(max_length=200)
    aapf_txn_currency = models.CharField(max_length=200)
    aapf_txn_datetime = models.CharField(max_length=200)
    aapf_txn_gw_ref = models.CharField(max_length=200)
    aapf_txn_gw_sc = models.CharField(max_length=200)
    aapf_txn_maskedInstr = models.CharField(max_length=200)
    aapf_txn_otherInfo = models.CharField(max_length=200)
    aapf_txn_payLink = models.CharField(max_length=200)
    aapf_txn_payScheme = models.CharField(max_length=200)
    aapf_txn_ref = models.CharField(max_length=200)
    aapf_txn_sc = models.CharField(max_length=200)
    aapf_txn_sc_msg = models.CharField(max_length=200)
    aapf_txn_signature = models.CharField(max_length=200)
    callback = models.CharField(max_length=200)





