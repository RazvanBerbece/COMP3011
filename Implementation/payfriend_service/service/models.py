from django.db import models

# Create your models here.

class Transactions(models.Model):
    TransactionId = models.CharField(max_length=80)           
    Value = models.FloatField()           
    CustomerEmail = models.CharField(max_length=80)                          
    Timestamp = models.DateTimeField()        
    Company = models.DateTimeField(max_length=80)                     

class Users(models.Model):
    Email = models.CharField(max_length=80)
    Password = models.CharField(max_length=80)   
    Salt = models.CharField(max_length=80)      