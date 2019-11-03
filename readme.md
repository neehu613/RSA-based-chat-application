Step 1)
	Run the following command to start the redis server:
		
		sudo docker run -p 6379:6379 -d redis:2.8

Step2)
	Start the ASGI channels server using the command

		python manage.py runserver