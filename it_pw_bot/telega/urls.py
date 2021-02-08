from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from .views import StartBot


app_name = 'telega'

urlpatterns = [
    path('startbot', (StartBot.as_view()), name='startbot'),
]
