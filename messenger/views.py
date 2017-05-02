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
    anonyMessages = Message.objects.filter(recipient=user, anonymous=True)
    messages = Message.objects.filter(recipient=user, anonymous=False)
    friends = User.objects.all()
    return render(request, 'messenger/home.html', {'Anony':anonyMessages, 'Messages':messages, 'Friends':friends})


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

        isAnonymous = request.POST.get("anonymous")
        if isAnonymous in ['send-anonymous']:
            msg.anonymous = True
        else:
            msg.anonymous = False

        hint1 = request.POST.get("hint1")
        hint2 = request.POST.get("hint2")
        hint3 = request.POST.get("hint3")
        msg.hint = hint1 + hint2 + hint3

        msg.save()
        return redirect("home")
    else:
        return render(request, 'messenger/home.html')


def guess(request):
    if request.method == 'POST':
        return redirect("messageDetail")
    else:
        user = request.user
        messages = Message.objects.filter(recipient=user)
        message = messages[0]
        hints = message.hint
        text = message.text
        return render(request, 'messenger/guess.html', {"text":text, "Hint":hints})


def messageDetail(request):
    if request.method == 'POST':
        return redirect('home')
    else:
        return render(request, 'messenger/messageDetail.html')

