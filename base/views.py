from django.shortcuts import render , redirect
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Room, Topic, Message, User
from django.contrib.auth import authenticate, login, logout
from .forms import RoomForm , UserForm, MyUserCreationForm

# rooms = [
#     {'id':1,'name':'lets learn python'},
#     {'id':2,'name':'lets learn css'},
#     {'id':3,'name':'lets learn c++'},
# ]

def loginpage(request):

    page = 'login'

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(email = email)
        except:
            messages.error(request, 'User does not exist.')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or password does not exist.')

    context = {'page':page}
    return render(request, 'base/login_register.html', context)

def registerPage(request):
    form = MyUserCreationForm()

    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.name = user.name.capitalize()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request,'An error occured during registration')
            


    context = {'form':form}
    return render(request, 'base/login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    room_count2 = (Room.objects.all()).count()
    rooms = Room.objects.filter(
        Q(topic__name__icontains = q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
        )
    
    topics = Topic.objects.all()[0:5]
    room_count = rooms.count()
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))[0:3]

    context = {'rooms': rooms, 'topics':topics, 'room_count': room_count,'room_count2': room_count2, 'room_messages':room_messages}
    return render(request,'base/home.html', context)

def room(request, pk):
    room = Room.objects.get(id = pk)
    room_messages = room.message_set.all()[0:3]
    participants = room.participants.all()
    if request.method == 'POST':
        messages = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body'),
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)

    context = {'room': room, 'room_messages': room_messages, 'participants':participants}
    return render(request,'base/room.html', context)


def userprofile(request, username):
    user = User.objects.get(username=username)
    rooms = user.room_set.all()
    room_count2 = (Room.objects.all()).count()
    room_messages = user.message_set.all()[0:3]
    topics = Topic.objects.all()
    context = {'user':user, 'rooms':rooms, 'room_messages':room_messages, 'topics':topics, 'room_count2':room_count2}
    return render(request, 'base/profile.html',context)

@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, creatd = Topic.objects.get_or_create(name=topic_name)

        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description'),
        )
        # form = RoomForm(request.POST)
        # if form.is_valid():
        #     room = form.save(commit=False)
        #     room.host = request.user
        #     room.save()
        return redirect('home')

    context = {'form' : form, 'topics': topics, 'room':room}
    return render(request, 'base/room_form.html', context)

@login_required(login_url='login')
def updateRoom(request , pk):
    room = Room.objects.get(id = pk)
    form = RoomForm(instance = room)

    if request.user != room.host:
        return HttpResponse('Your are not allowed here!!')

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, creatd = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        # form = RoomForm(request.POST, instance=room)
        # if form.is_valid():
        #     form.save()
        return redirect('home')
    topics = Topic.objects.all()
    context = {'form':form, 'topics':topics, 'room':room}
    return render(request, 'base/room_form.html', context)

@login_required(login_url='login')
def deleteRoom(request , pk):
    room = Room.objects.get(id = pk)

    if request.user != room.host:
        return HttpResponse('Your are not allowed here!!')

    if request.method == 'POST':
        room.delete()
        return redirect('home')        

    return render(request, 'base/delete.html', {'obj':room})

@login_required(login_url='login')
def deleteMessage(request , pk):
    messages = Message.objects.get(id = pk)

    if request.user != messages.user:
        return HttpResponse('Your are not allowed here!!')

    if request.method == 'POST':
        messages.delete()
        return redirect('home')        

    return render(request, 'base/delete.html', {'obj':messages})

@login_required(login_url='login')
def updateuser(request):
    user = request.user
    form = UserForm(instance=request.user)
    if request.method == 'POST':
        form = UserForm(request.POST,request.FILES,instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile',pk=user.id)
    context = {'form':form}
    return render(request,'base/update-user.html',context)

def topics_all(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(Q(name__icontains=q))
    context = {'topics':topics}
    return render(request,'base/topics.html', context)

def allUsers(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    users = User.objects.filter(Q(name__icontains=q) | Q(username__icontains=q))
    context = {'users':users}
    return render(request,'base/Users.html', context)