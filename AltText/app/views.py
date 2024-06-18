from django.shortcuts import render, redirect
import requests
from django.http import JsonResponse
from django.contrib.auth.models import User
from .models import SavedTexts
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
import json
from django.views import View
import base64
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("ALTTEXT_API_KEY")

# Create your views here.
class Signup(View):
    def get(self, request):
        if(request.user.is_authenticated):
            return redirect('/')
        
        return render(request, 'signup.html')
    
    def post(self, request):
        data = request.POST
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        password_confirm = data.get('password-confirm')

        if(password != password_confirm):
            return redirect('/signup')
        
        user = User.objects.create_user(username, email, password)

        return redirect('/signin')

class Signin(View):
    def get(self, request):
        if(request.user.is_authenticated):
            return redirect('/')
        
        return render(request, 'login.html')
    
    def post(self, request):
        data = request.POST
        username = data.get('username')
        password = data.get('password')
        
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/')

        return redirect('/signin')


class Home(LoginRequiredMixin, View):
    login_url='/signin'
    redirect_field_name=''

    def get(self, request):
        return render(request, 'home.html')
    
    def post(self, request):
        if 'imageInput' in request.FILES:
            image = request.FILES['imageInput']
            image_bytes = image.read()
            encoded_image = base64.b64encode(image_bytes).decode('utf-8')

            api_response = get_altText(encoded_image)

            return render(request, 'result.html', {'encoded_image': encoded_image, 'response': api_response, 'file_name': image.name})
        
        return redirect('/')
    

class Logout(View):
    def get(self, request):
        logout(request)
        return redirect('/signin')

class SaveText(View):
    def post(self, request):
        try:
            form_data = json.loads(request.body)
        except:
            return JsonResponse({'error': 'Invalid Form Data Format'}, status=400)
    
        try:
            filename = form_data.get('file_name')
            text = form_data.get('text')
        except:
            return JsonResponse({'error': 'Invalid Form'}, status=400)
    
        try:
            username = User.objects.get(username=request.user.username)
        except:
            return JsonResponse({'error': 'User Not Found'}, status=404)
        
        existing_saved_text = SavedTexts.objects.filter(filename=filename, username=username).first()

        if (existing_saved_text):
            existing_saved_text.text = text
            existing_saved_text.save()
            return JsonResponse({'success': 'Text has been saved'}, status=200)
        
        new_saved_data = SavedTexts(filename=filename, username=username, text=text)
        new_saved_data.save()

        return JsonResponse({'success': 'Text has been saved'}, status=200)
    
class Profile(LoginRequiredMixin, View):
    login_url='/signin'
    redirect_field_name=''
    def get(self, request):
        query_response = SavedTexts.objects.filter(username=request.user.id)
        saved_texts = [(saved_text.filename, saved_text.text) for saved_text in query_response]
        
        return render(request, 'profile.html', {'saved_texts': saved_texts})

def get_altText(base64_str):
    url = "https://alttext.ai/api/v1/images"

    payload = json.dumps({
        "image": {
            "raw": base64_str
        }
    })

    headers = {
        'Content-Type': 'application/json',
        'X-API-Key': api_key
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    return json.loads(response.text)['alt_text']