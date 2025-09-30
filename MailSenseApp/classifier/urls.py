from django.urls import path
from . import views

urlpatterns = [
    # A URL vazia ('') mapeia para a função classify_email na View
    path('', views.classify_email, name='classify'),
    path('clear-history/', views.clear_history, name='clear_history'),
]