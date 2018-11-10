from django.urls import path, re_path
from . import views

urlpatterns = [
    path('accueil', views.home),
    path('eleve/<str:idul>', views.view_eleve),
    path('articles/<int:year>/<int:month>', views.list_articles),  
    re_path(r'(?P<idul>^[A-Z]{5}\d{0,2}$)', views.view_eleve, name='eleve')
]