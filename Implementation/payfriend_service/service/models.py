from django.db import models

# Create your models here.

class Transaction(models.Model):
    TransactionId = models.CharField(max_length=80)           
    Value = models.FloatField()           
    CustomerEmail = models.CharField(max_length=80) 
    Company = models.CharField(max_length=80)                            
    Timestamp = models.FloatField()                          

class User(models.Model):
    Email = models.CharField(max_length=80)
    Password = models.CharField(max_length=80)   
    Salt = models.CharField(max_length=80)      