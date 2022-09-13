import datetime
from pickle import FALSE
from pyexpat import model
from statistics import mode
from django.db import models
from django.contrib.auth.models import User
from PIL import Image


sala_nr = (("", ""), ("1", "1"), ("2", "2"))

class reservas_Coworking_provisoria(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    startDate = models.DateField(null=True, blank=True)
    endDate = models.DateField(null=True, blank=True)
    nrDias = models.PositiveIntegerField(default=0)
    cost_price = models.FloatField(default=0.0)
    first_step = models.BooleanField(default=False)
    second_step = models.BooleanField(default=False)
    chair1 = models.BooleanField(default=False)
    chair2 = models.BooleanField(default=False)
    chair3 = models.BooleanField(default=False)
    chair4 = models.BooleanField(default=False)
    chair5 = models.BooleanField(default=False)
    chair6 = models.BooleanField(default=False)
    chair7 = models.BooleanField(default=False)
    chair8 = models.BooleanField(default=False)
    chair9 = models.BooleanField(default=False)
    chair10 = models.BooleanField(default=False)
    chair11 = models.BooleanField(default=False)
    chair12 = models.BooleanField(default=False)
    transactionId = models.CharField(max_length=500, null=True)

class Product(models.Model):
    nrLugares = models.IntegerField(default=0)
    startDate = models.DateField(null=True, blank=True)
    endDate = models.DateField(null=True, blank=True)
    nrDias = models.IntegerField(default=0)
    cost_price = models.IntegerField(default=0)
    active = models.BooleanField(default=False)
    chair1 = models.BooleanField(default=False)
    chair2 = models.BooleanField(default=False)
    chair3 = models.BooleanField(default=False)
    chair4 = models.BooleanField(default=False)
    chair5 = models.BooleanField(default=False)
    chair6 = models.BooleanField(default=False)
    chair7 = models.BooleanField(default=False)
    chair8 = models.BooleanField(default=False)
    chair9 = models.BooleanField(default=False)
    chair10 = models.BooleanField(default=False)
    chair11 = models.BooleanField(default=False)
    chair12 = models.BooleanField(default=False)


class reservas_Coworking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    nrLugares = models.IntegerField(default=0)
    startDate = models.DateField(null=True, blank=True)
    endDate = models.DateField(null=True, blank=True)
    nrDias = models.IntegerField(default=0)
    cost_price = models.FloatField(default=0.0)
    active = models.BooleanField(default=False)
    chair1 = models.BooleanField(default=False)
    chair2 = models.BooleanField(default=False)
    chair3 = models.BooleanField(default=False)
    chair4 = models.BooleanField(default=False)
    chair5 = models.BooleanField(default=False)
    chair6 = models.BooleanField(default=False)
    chair7 = models.BooleanField(default=False)
    chair8 = models.BooleanField(default=False)
    chair9 = models.BooleanField(default=False)
    chair10 = models.BooleanField(default=False)
    chair11 = models.BooleanField(default=False)
    chair12 = models.BooleanField(default=False)

    def get_display_price(self):
        return "{0:.2f}".format(self.cost_price / 100)
    
   
    

    def __str__(self):
        return str(self.user.username+" | "+str(self.startDate)+"-"+str(self.endDate))


class Price(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    stripe_price_id = models.CharField(max_length=100)
    price = models.IntegerField(default=0)

    def __str__(self):
        return str(self.product)


class meetingRooms(models.Model):
    ids = models.CharField(max_length=10, blank=True, choices=sala_nr)

    def __str__(self):
        return self.ids




class meetingRoomCalendar(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    sala = models.ForeignKey(meetingRooms, on_delete=models.CASCADE, null=True)
    date = models.DateField(null=True)
    startTime = models.TimeField()
    endTime = models.TimeField()
    cost_price = models.FloatField(default=0.0)

    def __str__(self):
        return str(self.user.username + " | " + str(self.date) + " | " + str(self.startTime) + " - " + str(self.endTime))




class meetingRoomProvisoria(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    sala = models.ForeignKey(meetingRooms, on_delete=models.CASCADE, null=True)
    date = models.DateField(null=True)
    startTime = models.TimeField()
    endTime = models.TimeField()
    cost_price = models.FloatField(default=0.0)
    transactionId = models.CharField(max_length=500, null=True)





class mensagen(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    date = models.DateTimeField(null=True)
    ClientName = models.CharField(max_length=30)
    Reason = models.CharField(max_length=50, default="contacto")
    ClientEmail = models.EmailField(max_length=100, default="")
    ClientMessage = models.CharField(max_length=500)
    Pendente = models.BooleanField(default=True)

    def __str__(self):
        return self.ClientName + " | " +  self.ClientMessage + " | Pending: " +  str(self.Pendente)


class gallery(models.Model):
    image = models.ImageField(upload_to='static/images')
    caption = models.CharField(max_length=200)

    def __str__(self):
        return self.caption


class Wallet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mettingRoomHours = models.IntegerField(default=0)
    mettingRoomMinutes = models.IntegerField(default=0)

    def __str__(self):
        return str(self.user.username + " | "+ str(self.mettingRoomHours)+":"+str(self.mettingRoomMinutes) + " hours")
    



class AcmeWebhookMessage(models.Model):
    payload = models.CharField(max_length=500,null=True)


class bundleProvisorio(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bundle_5 = models.BooleanField(default=False)
    bundle_10 = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=50, null=True)

    def __str__(self):
        if self.bundle_10 == True:
            return str(self.user.username + " | bundle 10"+ self.transaction_id)
        else:
            return str(self.user.username + " | bundle 5 | "+ self.transaction_id)

type = (("", ""), ("MBWAY", "MBWAY"), ("REFERENCE", "REFERENCE"), ("CARD", "CARD"))
status = (("", ""), ("Pending", "Pending"), ("Success", "Success"), ("Declined", "Declined"), ("Refunded", "Refunded"))

class transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    transactionId = models.CharField(max_length=500, null=True)
    status = models.CharField(max_length=50,null=True, choices=status)
    payment_Method = models.CharField(max_length=50,null=True, choices=type)
    price = models.FloatField(null=True)
    expireDate = models.DateTimeField(null=True)

    def __str__(self):
        return str(self.user.username + " | " + str(self.status) +  " | " + str(self.payment_Method) + " | "+ str(self.price)+ "€ | " + str(self.transactionId))


