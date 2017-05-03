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
    # anonyMessages = Message.objects.filter(recipient=user, anonymous=True)
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

    user = request.user
    messages = Message.objects.filter(recipient=user, anonymous=True)
    message = messages[0]
    hint = message.hint
    text = message.text
    sender = message.sender
    guess = request.POST.get("guess")
    counterPost = 0
    counterGet = 0
    if request.method == 'POST':
        count = counterPost + 1

        if (guess == sender.username) and (counterPost < 3):
            return render(request, "messenger/messageDetail.html", {"Username": guess, "text": text})
        elif (guess != sender.username) and (counterPost < 3):
            return redirect("guess")
        elif count > 3:
            displayString = "You have guessed three times."
            return render(request, "messenger/guess.html", {"Display": displayString})
    else:
        counterGet = counterGet + 1

        return render(request, 'messenger/guess.html', {"text":text, "Hint":hint, "Friends":friends})


def messageDetail(request):
    originalSender = request.GET.get("friendName")

    if request.method == 'POST':
        msg = Message()
        msg.text = request.POST.get("message")
        msg.anonymous = False
        msg.recipient = User.objects.get(username="Andrew")
        msg.sender = request.user
        msg.save()
        return redirect('home')
    else:
        return render(request, 'messenger/messageDetail.html')

