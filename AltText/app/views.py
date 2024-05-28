from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.views import View

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

        print(user)

        return redirect('/signin')
