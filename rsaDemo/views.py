import random, json
from . import crypt, genLargePrimes
from .models import messageModel, roomModel, userModel
from .forms import messageForm, roomForm, SignUpForm, passwordForm, verificationForm
from django.http import HttpResponseRedirect
from django.utils.safestring import mark_safe
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from datetime import datetime

def register(request):
	if(request.method == 'POST'):
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			uname = form.cleaned_data.get('username')
			raw_pass = form.cleaned_data.get('password1')
			user = authenticate(username=uname, password=raw_pass)
			login(request, user)
			return redirect('login')
	else:
		form = SignUpForm()
	return render(request, 'rsaDemo/register.html', {'form' : form})

@login_required
def home(request):
	return render(request, 'rsaDemo/home.html')

@login_required
def joinRoom(request):
	rooms = roomModel.objects.all()
	context = {
		'rooms' : rooms,
	}
	return render(request, 'rsaDemo/joinRoom.html', context)


def privateChat(request):
	users = userModel.objects.all()
	context = {
		'users' : users,
	}
	return render(request, 'rsaDemo/privateChat.html', context)

@login_required
def createRoom(request):
	form = roomForm(request.POST)
	if(request.method == 'POST'):
		if form.is_valid():
			roomName = form.cleaned_data['roomName']
			if not roomModel.objects.filter(roomName=roomName).exists():
				form.save()
				roomType = form.cleaned_data['roomType']
				if roomType == 'private':
					return redirect('rsaDemo:putPassword', room_name=roomName)

				messages.success(request, 'Room successfully created')
				return redirect('rsaDemo:room', room_name=roomName)
			else:
				messages.info(request, 'Room already exists')
				return redirect('rsaDemo:createRoom')
		else:
			messages.warning(request, 'Please correct the error below.')
	else:
		form = roomForm()
	return render(request, 'rsaDemo/createRoom.html', {'form': form}) 



def putPassword(request, room_name):
	room = roomModel.objects.get(roomName=room_name)
	form = passwordForm(request.POST)
	if request.method == 'POST':
		if form.is_valid():
			password = form.cleaned_data.get('password')
			room.password = password
			room.save()
			return redirect('rsaDemo:room', room_name=room_name)
	else:
		form = passwordForm()
	context = {
		'room' : room,
		'form' : form,
	}
	return render(request, 'rsaDemo/putPassword.html', context)

@login_required
def room(request, room_name):
	form = messageForm(request.POST)
	if request.method == 'POST':
		if form.is_valid():
			plaintext = form.cleaned_data['text']
			bitlength = form.cleaned_data['bits']
			form.save()
			rsaObj = messageModel.objects.get(text=plaintext)
			rsaObj.date = datetime.now()
			rsaObj.sender = request.user.username
			rsaObj.room = roomModel.objects.get(roomName=room_name)
			rsaObj.save(update_fields=['date', 'sender', 'room'])
			n, phi, private_key, public_key = crypt.runRSA(bitlength)
			ct_list, ciphertext = crypt.encrypt(plaintext, public_key, n)
			deciphered_text = crypt.decrypt(ct_list, ciphertext, private_key, n)
			rsaObj.modulus = n
			rsaObj.cipherText = ciphertext
			rsaObj.ctlist = json.dumps(ct_list)
			rsaObj.publicKey = str(public_key)
			rsaObj.phi = str(phi)
			rsaObj.save(update_fields=['modulus', 'cipherText', 'ctlist', 'publicKey', 'phi'])

			messages.success(request, "Message encrypted successfully. Your Private key is : " + str(private_key))
			context = {
				'form' : form,
				'plaintext' : plaintext,
				'ciphertext' : ciphertext,
				'ct_list' : ct_list,
				'modulus' : n,
				'phi' : phi,
				'private_key' : private_key,
				'public_key' : public_key,
				'room_name_json': (mark_safe(json.dumps(room_name))),
			}
			
	else:
		form = messageForm()
		context = {
			'form' : form,
			'room_name_json': (mark_safe(json.dumps(room_name))),
		}

	return render(request, 'rsaDemo/room.html', context)

@login_required
def send(request):
	form = messageForm(request.POST)
	
	if form.is_valid():
		plaintext = form.cleaned_data['text']
		bitlength = form.cleaned_data['bits']
		form.save()
	else:
		form = messageForm()
	context = {
		'form' : form,
	}
	return render(request, 'rsaDemo/send.html', context)

@login_required
def verifyIdentity(request, room_name):
	room = roomModel.objects.get(roomName=room_name)
	roompassword = str(room.password)
	form = verificationForm(request.POST)
	if request.method == 'POST':
		if form.is_valid():
			password = form.cleaned_data.get('password')
			if roompassword == str(password):
				return redirect('rsaDemo:room', room_name=room_name)
			else:
				messages.warning(request, 'Wrong password')
	else:
		form = verificationForm()
	context = {
		'room' : room,
		'form' : form,
	}
	return render(request, 'rsaDemo/verifyIdentity.html', context)

@login_required
def decrypt(request, room_name):
	room = roomModel.objects.get(roomName=room_name)
	messages = room.messagemodel_set.all().filter(read=False).order_by('-date')
	data = []
	if len(messages) == 0:
		flag=True
	else:
		flag=False
	print(flag)
	for item in messages:
		date_ = item.date
		date = str(date_.hour) + ":" + str(date_.minute) + ":" + str(date_.second)
		publickey_ = int(item.publicKey)
		modulus = int(item.modulus)
		totient = int(item.phi)
		cipherText_ = int(item.cipherText)
		bits = item.bits
		
		privateKey = crypt.generatePrivateKey(publickey_, totient)

		print("public key : ", publickey_)
		print("totient : ", totient)
		print("PRIVATE KEY : ", privateKey)

		jsonDec = json.decoder.JSONDecoder()
		ct_list = jsonDec.decode(item.ctlist)

		deciphered_text = crypt.decrypt(ct_list, cipherText_, privateKey, modulus)
		message_dict = {
			'ciphertext' : str(item.cipherText),
			'sender' : str(item.sender),
			'time' : str(date),
			'deciphered_text' : str(deciphered_text),
			'bits' : bits,
		}
		data.append(message_dict)
		item.read = True
		item.save(update_fields=['read'])

	context = {
		'data' : data,
		'flag' : flag,
		'room' : room_name,
	}

	print(context)

	return render(request, 'rsaDemo/decrypt.html', context)

@login_required
def chatlog(request, room_name):
	room = roomModel.objects.get(roomName=room_name)
	messages_ = room.messagemodel_set.all().filter(read=False)
	messages = room.messagemodel_set.all().filter(read=True).order_by('-date')

	if len(messages_):
		flag=True
	else:
		flag=False

	if len(messages) == 0:
		flag1=True
	else:
		flag1=False

	chat_log = []
	for item in messages:
		bits = item.bits
		sender = item.sender
		ciphertext = item.cipherText
		publicKey = item.publicKey
		time = item.date
		plaintext = item.text

		chat = {
			'bits' : bits,
			'sender' : sender,
			'ciphertext' : ciphertext,
			'publicKey' : publicKey,
			'time' : time,
			'plaintext' : plaintext,
		}

		chat_log.append(chat)
		
	context = {
		'chatlog':chat_log,
		'flag':flag,
		'flag1':flag1,
		'room' : room_name,
	}

	return render(request, 'rsaDemo/chatlog.html', context)
