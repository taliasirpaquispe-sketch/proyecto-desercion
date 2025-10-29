from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('formulario/', views.formulario, name='formulario'),
    path('historial/', views.historial, name='historial'),
    path('consultas/', views.consultas, name='consultas'),
    path('reportes/', views.reportes, name='reportes'),
    path('estadisticas/', views.estadisticas, name='estadisticas'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('export/csv/', views.export_studentrecords_csv, name='export_csv'),
    path('export/excel/', views.export_studentrecords_excel, name='export_excel'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]


