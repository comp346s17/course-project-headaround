# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from messenger.models import Message
from django.contrib.auth.models import User
# Create your views here.


def home(request):
    user = request.user
    messages = Message.objects.filter(recipient=user, anonymous=True)
    friends = User.objects.all()
    return render(request, 'messenger/home.html', {'Messages':messages, 'Friends':friends})


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'messenger/signup.html', {'form': form})


def logout(request):
    return render(request, 'messenger/login.html')


def message(request):
    if request.method == 'POST':

        msg = Message()
        msg.sender = request.user
        msg.text = request.POST.get("message")

        reciname = request.POST.get("recipient")
        reci = User.objects.filter(username=reciname)
        for r in reci:
            msg.recipient = r

        msg.anonymous = True

        msg.hint = request.POST.get("hint")

        msg.save()
        return redirect("home")
    else:
        return render(request, 'messenger/home.html')


def guess(request):
    friends = User.objects.all()
    message_id = request.GET.get('id')
    user = request.user
    message = Message.objects.get(id=message_id)
    hint = message.hint
    text = message.text
    sender = message.sender
    guess = request.POST.get("guess")
    messages = Message.objects.filter(sender=sender, recipient=user)
    if request.method == 'POST':
        if guess == sender.username:
            return render(request, "messenger/messageDetail.html", {"Username": guess, "Messages": messages})
        else:
            return redirect("home")
    else:
        return render(request, 'messenger/guess.html', {"text":text, "Hint":hint, "Friends":friends})


def messageDetail(request):
    if request.method == 'POST':
        msg = Message()
        msg.text = request.POST.get("message")
        msg.anonymous = False
        friend_id = request.GET.get('id')
        friend = User.objects.get(id=friend_id)
        msg.recipient = friend
        msg.sender = request.user
        msg.save()
        return redirect('home')
    else:
        friend_id = request.GET.get('id')
        friend = User.objects.get(id=friend_id)
        messages = Message.objects.filter(sender=friend)
        return render(request, 'messenger/messageDetail.html', {"Username":friend.username, "Messages":messages})
