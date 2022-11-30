
from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Person(models.Model):
	user = models.OneToOneField(User,null = True, on_delete=models.CASCADE)
	name = models.CharField(max_length=200, null=True)

	def __str__(self):
		return self.name

class Channel(models.Model):

    sender = models.OneToOneField(User,null = True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    people = models.ManyToManyField(Person,)
    message_data = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name

class DirectMessage(models.Model):
    #message sent by this person
    sender = models.OneToOneField(User,null = True, on_delete=models.CASCADE)
    #name will can be edited:
    name = models.CharField(max_length=200, null=True)
    #many to many but will only have 2 people / who can access this
    both_people = models.ManyToManyField(Person)
    #auto display
    message_data = models.CharField(max_length=200, null=True)
   

