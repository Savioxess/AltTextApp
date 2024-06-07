from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
import base64

# Create your views here.
class Signup(View):
    def get(self, request):
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

            return render(request, 'result.html', {'encoded_image': encoded_image, 'response': test_api_response.get('response')})
        
        return redirect('/')

class Logout(View):
    def get(self, request):
        logout(request)
        return redirect('/signin')