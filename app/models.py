from django.db import models
from django.contrib.auth.models import User


class Producer (models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Device (models.Model):
    name = models.CharField(max_length=50)
    producer = models.ForeignKey(
        Producer, related_name='device', on_delete=models.CASCADE, blank=True)
    isEOL = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Week (models.Model):
    start = models.DateField(auto_now=False, auto_now_add=False)
    end = models.DateField(auto_now=False, auto_now_add=False)

    def __str__(self):
        return str(self.id)


class Sale (models.Model):
    device = models.ForeignKey(
        Device, related_name='sales', on_delete=models.CASCADE)
    week = models.ForeignKey(Week, related_name='sales',
                             on_delete=models.CASCADE)
    amount = models.IntegerField(null=True)

    def __str__(self):
        return str(self.id)


class PredictedSale (models.Model):
    device = models.ForeignKey(
        Device, related_name='predicted', on_delete=models.CASCADE)
    week = models.ForeignKey(Week, related_name='predicted',
                             on_delete=models.CASCADE)
    amount = models.IntegerField(null=True)

    def __str__(self):
        return self.device.name + '-' + str(self.week.id)


class Transaction (models.Model):
    transactionType = models.CharField(max_length=10)
    device = models.ForeignKey(
        Device, related_name='transactions', on_delete=models.CASCADE)
    transactionDate = models.DateTimeField(auto_now=False, auto_now_add=True)
    amount = models.IntegerField()

    def __str__(self):
        return str(self.id)


class Campaign (models.Model):
    start = models.DateField()
    end = models.DateField()
    amount = models.IntegerField()
    
    device = models.ForeignKey(
        Device, related_name='campaigns', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)
