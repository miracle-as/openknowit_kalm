from django.shortcuts import render
from .models import maindata, service, project

from rest_framework import viewsets


def mainview(request):
    maindata_entries = maindata.objects.all()
    maindata_services = service.objects.all()
    maindata_projects = project.objects.all()
    return render(request, 'main.html', {'maindata_entries': maindata_entries, 'title': 'IGN8', 'maindata_services': maindata_services , 'maindata_projects': maindata_projects})

def projectsview(request):
    myprojects = project.objects.all()
    return render(request, 'projects.html', {'maindata_entries': myprojects, 'title': 'Projects'})

def projectdetail(request, id):
    myproject = project.objects.get(pk=id)
    return render(request, 'projectdetail.html', {'maindata_entries': myproject, 'title': 'Project Detail'})    


