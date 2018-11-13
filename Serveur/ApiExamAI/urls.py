from django.urls import path, re_path
from . import views

urlpatterns = [
    path('accueil', views.home, name='Acceuil'),
    path('Acceuil_eleve', views.Acceuil_eleve, name="Acceuil_eleve"),
    path('statistiques', views.stats, name='stats'),
    path('connection-<str:idul>', views.connection, name='connection'),
    path('Aide', views.Aide, name="Aide"),
    re_path(r'^eleve/(?P<idul>[A-Z]{5}\d{0,2}$)',
            views.view_eleve, name='eleve')
]
