from django.urls import path, re_path
from . import views
from .views import KeyApi

app_name = 'ApiExamAI'

urlpatterns = [
    path('home/', views.home, name="home"),
    path('getKey/<str:idul>/', KeyApi.as_view(), name="getKey"),
    path('connection/<str:idul>', views.connection, name='connection'),
    path('sendVideoBuffer/<str:idul>', views.getBuffVideo, name='videoBuffer'),
    path('sendAudioBuffer/<str:idul>', views.getBuffAudio, name='audioBuffer'),
]
