from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.log_in, name='login'),
    path('logout/', views.log_out, name='exit'),
    #  La route VIP pour accéder à ton tableau de bord !
    path('dashboard/', views.dashboard_view, name='dashboard'),
]