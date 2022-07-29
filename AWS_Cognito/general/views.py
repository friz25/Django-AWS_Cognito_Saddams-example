from django.shortcuts import render
from decouple import config # читает данные из .env файлов
from . import decode_jwt
import base64
import requests


def home(request): # <WSGIRequest: GET '/?code=72XXXXX-ad82-4db4-8c79-a43103fcf414'>
    context = {}
    try:
        code = request.GET.get('code') #72XXXXX-ad82-4db4-8c79-a43103fcf414
        userData = getTokens(code)
        context['name'] = userData['name']
        context['status'] = 1
        print(f'{context=}')
        response = render(request, 'index.html', context)
        # response.set_cookie(key, value, max_age)
        response.set_cookie('sessiontoken', userData['id_token'], max_age=60*60*24, httponly=True)
        return response
    except:
        token = getSession(request)
        if token is not None:
            userData = decode_jwt.lambda_handler(token, None)
            context['name'] = userData['name']
            context['status'] = 1
            print(f'2){context=}')
            return render(request, 'index.html', context)
        return render(request, 'index.html', {'status': 0})


def getTokens(code):
    TOKEN_ENDPOINT = config('TOKEN_ENDPOINT') # 'https://deXXXXX.auth.eu-central-1.amazoncognito.com/oauth2/token'
    REDIRECT_URI = config('REDIRECT_URI') # 'http://localhost:8000/'
    CLIENT_ID = config('CLIENT_ID') # '7bjaXXXXXX7gbqXXX30vrrek8'
    CLIENT_SECRET = config('CLIENT_SECRET') # '1sb5bvrXXXXXXXXXXXXXo7giqf54ltnu2htjs9vkaegsg1l3u'

    encodeData = base64.b64encode(bytes(f"{CLIENT_ID}:{CLIENT_SECRET}", "ISO-8859-1")).decode("ascii") #'N2JqYWpvbWpkN2dicXXXXXXXzB2cnJlazg6MXNiNWJ2cnEzMW8xdjYyaXIzMjZsdnFvN2dpcWY1NGx0bnUyaHRqczl2a2FlZ3NnMWwzdQ=='

    headers = { #{'Content-Type': 'application/x-www-form-urlencoded', 'Authorization': 'Basic N2JqYWpvbWpkN2dicXXXXXXXXcnJlazg6MXNiNWJ2cnEzMW8xdjYyaXIzMjZsdnFvN2dpcWY1NGx0bnUyaHRqczl2a2FlZ3NnMWwzdQ=='}
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': f'Basic {encodeData}'
    }

    body = {
        'grant_type': 'authorization-code',
        'client_id': CLIENT_ID,
        'code': code,
        'redirect_uri': REDIRECT_URI,
    }

    response = requests.post(TOKEN_ENDPOINT, data=body, headers=headers) # 400 = BAD (here's there the ERROR is)

    id_token = response.json()['id_token']

    userData = decode_jwt.lambda_handler(id_token, None)

    if not userData:
        return False

    user = {
        'id_token': id_token,
        'name': userData['name'],
        'email': userData['email']
    }
    return user

def getSession(request):
    try:
        response = request.COOKIES['sessiontoken']
        return response
    except:
        return None

def signout(request):
    response = render(request, 'index.html', {'status': 0})
    response.delete_cookie('sessiontoken')
    return response