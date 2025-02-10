from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name='home'),
    path('reservation-page', views.reservation, name='reservation-page'),
]
