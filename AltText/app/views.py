from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.models import User
from .models import SavedTexts
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
import json
from django.views import View
import base64

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

            test_api_response = {
                'response': 'This image is a beautiful digital artwork depicting a landscape scene at sunset. The sky is filled with vibrant colors ranging from deep blues to bright oranges and pinks, creating a dramatic and colorful cloudscape. In the foreground, there is a leafless tree with branches stretching across the scene, casting shadows and adding depth to the image. The sunlight is seen near the horizon, casting a warm glow across the snow-covered landscape. In the background, there are mountains with sharp peaks and ridges, enhancing the sense of vastness and natural beauty. The overall composition blends elements of nature with an artistic, almost surreal touch, emphasizing the striking colors and serene atmosphere.'
            }

            return render(request, 'result.html', {'encoded_image': encoded_image, 'response': test_api_response.get('response'), 'file_name': image.name})
        
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