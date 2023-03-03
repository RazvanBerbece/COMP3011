from django.db import models

# Create your models here.

class Transaction(models.Model):
    source = models.CharField(max_length=80)                # source PayPal user account paying
    destination = models.CharField(max_length=80)           # destination business name (airline company)
    value = models.IntegerField()                           # value of transaction
    payment_method = models.CharField(max_length=30)        # chosen payment method (card, account balance)
    timestamp = models.DateTimeField()                      # UTC.Now timestamp when Transaction was started

class Card(models.Model):
    name = models.CharField(max_length=80)                  # name on card (encrypted)
    card_number = models.CharField(max_length=80)           # 16-digit PAN number on card (encrypted)
    expiration_date = models.CharField(max_length=80)       # expiration date on card (encrypted)