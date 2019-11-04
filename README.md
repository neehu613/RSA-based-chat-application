# RSA-based-chat-application
A django based chat application where you can send messages encrypted using RSA algorithm.

Make sure you install all dependencies first.
Open the project directory and run the following commands:
```
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
```

Run the local server using the command
```
sudo docker run -p 6379:6379 -d redis:2.8
python manage.py runserver
```

