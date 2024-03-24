from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.db.models import Q
from .models import CustomUser
from .forms import SignUpForm
from dotenv import load_dotenv
from django.contrib.auth import logout
import os
import json
import base64
from requests import post, get


# Create your views here.

def get_token():
    client_id = "34feb190cc0f4876b1b962313ac49396"
    client_secret = "70449f31f55c434b914f078fae8d5a4a"
    auth_string = f"{client_id}:{client_secret}"
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = base64.b64encode(auth_bytes).decode("utf-8")
    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    result = post(url, headers=headers, data=data)
    json_result = result.json()
    token = json_result.get("access_token")
    return token

def get_auth_header(token):
    return {"Authorization": f"Bearer {token}"}


def home(request):
    if request.user:
        print(request.user)
        token = get_token()
        headers = get_auth_header(token)
        url = f'https://api.spotify.com/v1/albums?ids=382ObEPsp2rxGrnsizN5TX%2C1A2GTWGtFfWp7KSQTwWOyo%2C2noRn2Aes5aoNVsU6iWThc'
        result = get(url, headers=headers)
        json_result = json.loads(result.content)
        albums = json_result.get('albums', [])  # Get albums if 'albums' key exists, otherwise default to an empty list
        return render(request, 'Harmony/home.html', {'songs': albums})
    else:
        return HttpResponse('over')
        # return redirect('login')



def login_view(request):
    if request.method == "POST":
        username_or_email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Check if user exists with provided username or email and password
        if CustomUser.objects.filter((Q(username=username_or_email) | Q(email=username_or_email)) & Q(password=password)).exists():
            user = CustomUser.objects.get(Q(username=username_or_email) | Q(email=username_or_email))
            # Log in the user
            login(request, user)
            return redirect('/home')
        else:
            return HttpResponse('Invalid username or password', status=401)  # Unauthorized status
    else:
        return render(request, 'Harmony/login.html')

def signup(request):
    if request.method=="POST":
        username=request.POST.get('username')
        email=request.POST.get('email')
        password=request.POST.get('password')
        user=User.objects.create_user(username=username,email=email,password=password)
        user.save()
        return render(request, 'Harmony/login.html')
    else:
        return render(request, 'Harmony/signup.html')


# @login_required(login_url='login')
def myartists(request):
    if request.user:
        token = get_token()
        headers = get_auth_header(token)
        url = f'https://api.spotify.com/v1/artists?ids=2CIMQHirSU0MQqyYHq0eOx%2C57dN52uHvrHOxijzpIgu3E%2C1vCWHaC5f2uS3yhpwWbIA6'
        result = get(url, headers=headers)
        json_result=json.loads(result.content)
        # print(json_result)
        artists = json_result['artists']  # Assuming the songs are in the 'songs' key in the response
        return render(request, 'Harmony/artists.html', {'artists': artists})
    else:
        return render(request, 'Harmony/login.html')
        


def search(request):
    if request.user:
        if "q" in request.GET:
            term = request.GET.get("q")
            token = get_token()
            headers = get_auth_header(token)
            url = f'https://api.spotify.com/v1/search?q={term}&type=track%2Cartist'
            result = get(url, headers=headers)
            json_result=json.loads(result.content)
            # print(json_result)
            # json_result = result.json()
            return JsonResponse(json_result)  # Just for testing, you should handle this data appropriately
        else:
            return render(request, 'Harmony/search.html')
    else:
        return render(request, 'Harmony/login.html')

@login_required
def my_protected_view(request):
    # Your protected view logic here
    pass

def landing_page(request):
    return render(request, 'Harmony/index.html')

def logout_view(request):
    logout(request)
    return redirect('login') 