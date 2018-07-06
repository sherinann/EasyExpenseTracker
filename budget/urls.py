from django.contrib import admin
from django.urls import path, include

from budget import views

urlpatterns = [
    path('all', views.get_budget, name="get_budget"),
]
