from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from .views import Signup, Signin, Home, Logout, SaveText, History, DownloadCSV

urlpatterns = [
    path('signup/', Signup.as_view(), name="signup"),
    path('signin/', Signin.as_view(), name="signin"),
    path('logout/', Logout.as_view(), name="logout"),
    path('saveText/', SaveText.as_view(), name="savetext"),
    path('history/', History.as_view(), name="profile"),
    path('download-history/', DownloadCSV.as_view(), name='download-csv'),
    path('', Home.as_view(), name="home")
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)