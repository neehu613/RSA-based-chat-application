# RSA-based-chat-application
A django based chat application where you can send messages encrypted using RSA algorithm.

Make sure you install all dependencies first.
Open the project directory and run the following commands:
```
pip install django
pip install channels
pip install channels-redis
pip install redis
```

Setting up the database:
```
python manage.py makemigrations
python manage.py migrate
```

Run the local server using the command
```
sudo docker run -p 6379:6379 -d redis:2.8
python manage.py runserver
```

## Usage and snapshots


You can set up your account by entering details in the registration form.

![Alt text](/screenshots/1Register.png?raw=true)



After you sign up, it takes you to the login page where you can enter your credentials and log in.

![Alt text](/screenshots/2Login.png?raw=true)



After successful login, it takes you to the home page. This application provides 2 main features.
* Creating Chatrooms - private/public
* Joining Chatrooms

It also displays the registered users.

![Alt text](/screenshots/3HomePage.png?raw=true)



Click on the __Create Room__ button and then enter the room name. You can create private/public rooms.

![Alt text](/screenshots/4CreateRoom.png?raw=true)



For private rooms, it needs a password

![Alt text](/screenshots/5PutPassword.png?raw=true)



The below image shows the __room__ page and you can enter your message inside the box provided on the right side. Once the message has been typed, you can click on the __Encrypt__ button to encrypt your message. You can perform encryption using different sized keys(128 bits, 256, 512, 1024, 2048)

![Alt text](/screenshots/6Room.png?raw=true)



The encryption process can be seen on the terminal output. It generates a public key and encrypts your message using it.

![Alt text](/screenshots/7Seeoutput.png?raw=true)

![Alt text](/screenshots/8seeoutput.png?raw=true)



You can open up an __incognito__ window and login with another user's credentials and join the same room. When the other user finishes encryption, he can hit the __SEND ENCRYPTED MESSAGE__ button to send the encrypted message. The user on the __incognito__ window can hit the __DECRYPT__ button to create a private key using the public key with which the message was encrypted and can decrypt the message.

![Alt text](/screenshots/9otherUser.png?raw=true)



The other user gets the public key used along with the enciphered text.

![Alt text](/screenshots/10ciphertext.png?raw=true)



On clicking the __DECRYPT__ button, it takes us to this page

![Alt text](/screenshots/11decrypt.png?raw=true)



You can view the decrypted message here

![Alt text](/screenshots/12decrypt.png?raw=true)



All the messages which have been decrypted are stored in a chat log.

![Alt text](/screenshots/13chatlog.png?raw=true)
