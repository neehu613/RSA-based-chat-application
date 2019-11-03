from django.db import models
from django.contrib.auth.models import User
from datetime import datetime 

bitlength_choices = (
	(128, '128 bits'),
	(256, '256 bits'),
	(512, '512 bits'),
	(1024, '1024 bits'),
	(2048, '2048 bits'),
)

roomType_choices = (
	("private", "private"),
	("public", "public"),
)


class userModel(User):
	user = models.OneToOneField(User,on_delete=models.CASCADE)
	uid = models.BigAutoField(primary_key=True)
	
	def __str__(self):
		return self.user.username

class roomModel(models.Model):
	roomId = models.BigAutoField(primary_key=True)
	roomName = models.CharField(max_length=200, unique=True)
	roomType = models.CharField(max_length=50,choices=roomType_choices, default="private")
	createdOn = models.DateTimeField(default=datetime.now, blank=False)
	password = models.CharField(max_length=100, default="")

	def __str__(self):
		return self.roomName

class createsModel(models.Model):
	uid = models.ForeignKey(userModel, on_delete=models.CASCADE) # needs to be a user
	roomId = models.ForeignKey(roomModel, on_delete=models.CASCADE) # needs to be a room 

class messageModel(models.Model):
	messageId = models.BigAutoField(primary_key=True)
	room = models.ForeignKey(roomModel, on_delete=models.CASCADE, null=True)
	text = models.TextField(blank=True, null=True)
	bits = models.IntegerField(choices=bitlength_choices, default='128')
	cipherText = models.TextField(blank=True, null=True)
	sender = models.CharField(max_length=200, default="")
	date = models.DateTimeField(default=datetime.now, editable=True)
	read = models.BooleanField(default=False)
	ctlist = models.TextField(blank=True, null=True)
	publicKey = models.TextField(blank=True, null=True)
	phi = models.TextField(blank=True, null=True)
	modulus = models.TextField(blank=True, null=True)

class roomHasMessages(models.Model):
	roomId = models.ForeignKey(roomModel, on_delete=models.CASCADE) # needs to be a room 
	messageId = models.ForeignKey(messageModel, on_delete=models.CASCADE) # needs to be a room 
