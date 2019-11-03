from django.urls import path
from . import views


app_name = 'rsaDemo'
urlpatterns = [
	path('', views.register, name='register'),
    path('send/', views.send, name='send'),
    path('home/', views.home, name='home'),
    path('home/joinRoom', views.joinRoom, name='joinRoom'),
    path('home/privateChat', views.privateChat, name='privateChat'),
    path('home/createRoom/', views.createRoom, name='createRoom'),
    path('home/createRoom/<str:room_name>/', views.room, name='room'),
    path('home/createRoom/<str:room_name>/chat-log', views.chatlog, name='chat-log'),
    path('home/createRoom/<str:room_name>/decrypt', views.decrypt, name='decrypt'),
    path('home/createRoom/<str:room_name>/verifyIdentity', views.verifyIdentity, name='verifyIdentity'),
    path('home/createRoom/<str:room_name>/putPassword', views.putPassword, name='putPassword'),
]
