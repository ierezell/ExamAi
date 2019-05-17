from Crypto.PublicKey import RSA
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Eleve
from .forms import photoForm, videoBufferForm, audioBufferForm


def home(request):
    return render(request, "ApiExamAI/home.html")


def connection(request, idul):
    eleve = get_object_or_404(Eleve, idul=idul)
    if request.method == 'POST':
        form = photoForm(request.POST, request.FILES, instance=eleve)
        print(form.data)
        print()
        print()
        print("Yoooooo", form.errors)
        if form.is_valid():
            print("Whouhouuuuuu")
            eleve = form.save()
            return HttpResponseRedirect(reverse('ApiExamAI:home'))
    else:
        form = photoForm(instance=eleve)
    return render(request, 'ApiExamAI/post_file.html', {'form': form})


def getBuffVideo(request, idul):
    eleve = get_object_or_404(Eleve, idul=idul)
    if request.method == 'POST':
        form = videoBufferForm(request.POST, request.FILES, instance=eleve)
        print(form.data)
        print()
        print()
        print("Yoooooo", form.errors)
        if form.is_valid():
            print("Whouhouuuuuu")
            eleve = form.save()
            return HttpResponseRedirect(reverse('ApiExamAI:home'))
    else:
        form = videoBufferForm(instance=eleve)
    return render(request, 'ApiExamAI/post_file.html', {'form': form})


def getBuffAudio(request, idul):
    eleve = get_object_or_404(Eleve, idul=idul)
    if request.method == 'POST':
        form = audioBufferForm(request.POST, request.FILES, instance=eleve)
        print(form.data)
        print()
        print()
        print("Yoooooo", form.errors)
        if form.is_valid():
            print("Whouhouuuuuu")
            eleve = form.save()
            return HttpResponseRedirect(reverse('ApiExamAI:home'))
    else:
        form = audioBufferForm(instance=eleve)
    return render(request, 'ApiExamAI/post_file.html', {'form': form})


class KeyApi(APIView):
    def get(self, request, idul):
        eleve = get_object_or_404(Eleve, idul=idul)
        new_key = RSA.generate(2048)
        private_key = new_key.exportKey()
        public_key = new_key.publickey().exportKey()
        eleve.clee_prive_serveur = private_key
        return Response(public_key)

    def post(self, request, idul):
        return Response(status=status.HTTP_202_ACCEPTED)

# @login_required


# @api_view(['GET'])
# def getKey(request, idul):
#     eleve = get_object_or_404(Eleve, idul=idul)
#     new_key = RSA.generate(2048)
#     private_key = new_key.exportKey()
#     public_key = new_key.publickey().exportKey()
#     eleve.clee_prive_serveur = private_key
#     return Response(public_key)
