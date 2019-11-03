from django import forms
from .models import messageModel, roomModel, userModel
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
	first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
	last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
	
	class Meta:
		model = userModel
		fields = ('username', 'first_name', 'last_name', 'password1', 'password1',)

class messageForm(forms.ModelForm):
	
	class Meta:
		model = messageModel
		fields = ('text', 'bits')

	def __init__(self, *args, **kwargs):
		super(messageForm, self).__init__(*args, **kwargs)
		self.fields['text'].widget.attrs\
			.update({
				'id': 'chat-message-input',
				'placeholder': 'Enter your message here\n\nAlways encrypt after typing your message'
			})

class roomForm(forms.ModelForm):
	class Meta:
		model = roomModel
		fields = ('roomName', 'roomType')

class passwordForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput)
	class Meta:
		model = roomModel
		fields = ('password',)

	def save(self, commit=True):
	    # Save the provided password in hashed format
	    room = super(passwordForm, self).save(commit=False)
	    room.set_password(self.cleaned_data["password"])
	    if commit:
	        room.save()
	    return room

class verificationForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput)
	class Meta:
		model = roomModel
		fields = ('password',)
	