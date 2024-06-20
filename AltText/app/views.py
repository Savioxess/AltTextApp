from django.shortcuts import render, redirect, HttpResponse
import datetime
import csv
import io
import requests
from django.utils import timezone
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
        
        new_saved_data = SavedTexts(filename=filename, username=username, text=text)
        new_saved_data.save()

        return JsonResponse({'success': 'AltText has been saved'}, status=200)
    
class History(LoginRequiredMixin, View):
    login_url='/signin'
    redirect_field_name=''
    def get(self, request):
        start_date_str = request.GET.get('start-date', '')
        end_date_str = request.GET.get('end-date', '')
        image_name = request.GET.get('image_name', '')

        query_response = get_filtered_data(request.user.id, start_date_str, end_date_str, image_name)

        csv_file_response = get_csv_file_response(query_response)
        saved_texts = [(saved_text.filename, saved_text.text, saved_text.date) for saved_text in query_response]

        return render(request, 'history.html', {'saved_texts': saved_texts, 'csv_file': csv_file_response})
    
class DownloadCSV(View):
    def post(self, request):
        csv_content = request.POST.get('csv_content', '')

        response = HttpResponse(csv_content, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="saved_alttexts_history.csv"'

        return response

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

def get_csv_file_response(saved_alttexts):
    buffer = io.StringIO()
    writer = csv.writer(buffer)

    writer.writerow(['image_name', 'alt_text', 'date'])

    for saved_alttext in saved_alttexts:
        writer.writerow([
            saved_alttext.filename,
            saved_alttext.text,
            saved_alttext.date,
        ])
    
    csv_content = buffer.getvalue()
    buffer.close()

    return csv_content

def get_filtered_data(userid, start_date_str, end_date_str, image_name):
    query_response = None

    if (start_date_str != '' and end_date_str != ''):
        start_date_naive = datetime.datetime.strptime(start_date_str, '%Y-%m-%d')
        end_date_naive = datetime.datetime.strptime(end_date_str, '%Y-%m-%d')
        start_date = timezone.make_aware(start_date_naive, timezone.get_current_timezone())
        end_date = timezone.make_aware(end_date_naive.replace(hour=23, minute=59, second=59), timezone.get_current_timezone())

        if (image_name != ''):
            query_response = SavedTexts.objects.filter(username=userid, date__gte=start_date, date__lte=end_date, filename=image_name)
        else: 
            query_response = SavedTexts.objects.filter(username=userid, date__gte=start_date, date__lte=end_date)
    elif (image_name != ''):
        query_response = SavedTexts.objects.filter(username=userid, filename=image_name)
    else:
        query_response = SavedTexts.objects.filter(username=userid)

    return query_response