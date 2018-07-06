from django.urls import path, include

from userprofile import views

urlpatterns = [
    path('otp/', views.get_otp, "get_otp")
]