from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import db
import json


def home(request):
    print request.body
    return render(request, 'is.html')


# ----- META API ------

def typeNodeEditor(request):
    rels = db.getRelationshipTypeNames()
    types = db.getTypeNames()
    return render(request, 'typeNodeEditor.html', {"rels":rels, "types":types})
