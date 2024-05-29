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

            return render(request, 'result.html', {'encoded_image': encoded_image})
        
        return redirect('/')

class Logout(View):
    def get(self, request):
        logout(request)
        return redirect('/signin')