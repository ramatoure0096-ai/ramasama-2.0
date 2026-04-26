from django.urls import path
from . import views

urlpatterns = [
    # Authentification
    path('login/', views.log_in, name='login'),
    path('logout/', views.log_out, name='exit'),

    # Dashboard & Ventes
    path('', views.dashboard_view, name='dashboard'),
    path('ventes/', views.liste_ventes, name='liste_ventes'),
    path('ventes/ajouter/', views.ajouter_vente, name='ajouter_vente'),
    
    # Exportation
    path('export/confirmation/', views.export_confirm, name='export_confirm'),
]