from django.db import models

# Create your models here.

class Transaction(models.Model):
    TransactionId = models.CharField(max_length=80)           
    Value = models.FloatField()           
    CustomerEmail = models.CharField(max_length=80) 
    Company = models.CharField(max_length=80)      
    City = models.CharField(max_length=80)   
    Postcode = models.CharField(max_length=80)   
    Country = models.CharField(max_length=80)   
    SourceCurrency = models.CharField(max_length=5)   
    SysCurrency = models.CharField(max_length=5)                       
    Timestamp = models.FloatField()                          

class User(models.Model):
    Email = models.CharField(max_length=80)
    Password = models.CharField(max_length=80)   
    Salt = models.CharField(max_length=80)      