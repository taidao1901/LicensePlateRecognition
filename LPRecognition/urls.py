from django.conf import settings
from django.views.static import serve
from django.urls import path 
from . import views
from django.views.generic import RedirectView
from django.conf.urls.static import static  

urlpatterns =[  
    path('', views.detect_request),
    path('api_request/',views.LPRecognition_api),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)