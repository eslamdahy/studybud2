from django.urls import path
from . import views

urlpatterns = [ 
    path('login/', views.loginpage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.registerPage, name='register'),

    path('', views.home, name='home'),
    path('room/<str:pk>/', views.room, name='room'),
    path('profile/<str:username>/', views.userprofile, name='user-profile'),

    path ('createRoom/', views.createRoom, name='createRoom'),
    path ('updateRoom/<str:pk>', views.updateRoom, name='updateRoom'),
    path ('deleteRoom/<str:pk>', views.deleteRoom, name='deleteRoom'),
    path ('deleteMessage/<str:pk>', views.deleteMessage, name='deleteMessage'),
    path ('update-user/', views.updateuser, name='update-user'),
    path ('all-topics/', views.topics_all, name='all-topics'),
    path ('all-Users/', views.allUsers, name='all-Users'),
]