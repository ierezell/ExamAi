from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404
from django.shortcuts import redirect
from datetime import datetime


def list_articles(request, year, month):
    if month > 12:
        #return redirect(view_eleve, idul='PISNE')
        return redirect('eleve', idul='PISNE')
        #return redirect("https://www.djangoproject.com")
    else :
        return HttpResponse(
        "Vous avez demandé {0} et {1} !".format(year,month))

def home(request):
    return HttpResponse("""
        <h1>Bienvenue ExamAi !</h1>
        <p>Api : getInfos ou plop </p>
    """)

def view_eleve(request, idul):
    #return HttpResponse("Vous avez demandé l'eleve {0} !".format(idul))
    date = datetime.now()
    #eturn render(request, 'ApiExamAI/eleve.html', date)
    return render(request, 'ApiExamAI/eleve.html', locals())
