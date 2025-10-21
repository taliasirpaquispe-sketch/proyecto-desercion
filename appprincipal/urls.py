from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('formulario/', views.formulario, name='formulario'),
    path('historial/', views.historial, name='historial'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('estadisticas/', views.estadisticas, name='estadisticas'),



]
