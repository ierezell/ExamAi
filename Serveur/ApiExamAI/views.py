from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from datetime import datetime
from Crypto.PublicKey import RSA
from . import models


def home(request):
    return HttpResponse("""
        <h1>Bienvenue ExamAi !</h1>
        <p>Api : getInfos ou plop </p>
    """)


def Acceuil_eleve(request):
    return render(request, 'ApiExamAI/Acceuil_eleve.html')


def view_eleve(request, idul="AAAAA"):
    # return HttpResponse("Vous avez demandé l'eleve {0} !".format(idul))
    date = datetime.now()
    # return render(request, 'ApiExamAI/eleve.html', date)
    return render(request, 'ApiExamAI/eleve.html', locals())


def stats(request):
    return render(request, 'ApiExamAI/stats.html')


def Aide(request):
    return render(request, 'ApiExamAI/Aide.html')


def connection(request, idul):
    eleve = models.Eleve(idul=idul)
    eleve.clee = RSA.generate(4096).publickey()
    #eleve.surveille.suspect = 0
    # public_key.encrypt(TrucQuonVeutSecuriser)
