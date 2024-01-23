
from django.urls import path, include
from .views import  mainview, projectdetail
from rest_framework.routers import DefaultRouter



urlpatterns = [
    path('', mainview, name='ignite_home'),
    path('project/<id>', projectdetail,  name='project_detail'),

]