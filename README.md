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

Setting up of the database:
```
python manage.py makemigrations
python manage.py migrate
```

Run the local server using the command
```
sudo docker run -p 6379:6379 -d redis:2.8
python manage.py runserver
```

