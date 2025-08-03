from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.add_vectors, name='add_vectors'),
]
