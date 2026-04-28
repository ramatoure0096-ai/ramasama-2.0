from django.urls import path
from . import views

urlpatterns = [
    path('', views.log_in, name='login'),
    path('logout/', views.log_out, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard_view'),
    path('ventes/', views.vente_list_view, name='vente_list'),
    path('ventes/ajouter/', views.vente_create_view, name='vente_create'),
    path('ventes/supprimer/<int:pk>/', views.vente_delete_view, name='vente_delete'),
    path('ventes/recu/<int:pk>/', views.recu_vente_view, name='export_pdf'), # Le lien magique
    path('produits/ajouter/', views.produit_create_view, name='produit_create'),
    path('produits/modifier/<int:pk>/', views.produit_edit_view, name='produit_edit'),
]