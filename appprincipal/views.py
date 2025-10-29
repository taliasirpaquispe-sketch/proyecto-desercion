from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Student, AnalysisResult
from django.db.models import Avg, Count
import random
from datetime import datetime, timedelta

# =========================================================
# PANTALLA PRINCIPAL
# =========================================================
@login_required
def inicio(request):
    registros = AnalysisResult.objects.all().order_by('-id')[:5]
    return render(request, 'inicio.html', {'registros': registros})


# =========================================================
# FORMULARIO DE ANÁLISIS
# =========================================================
@login_required
def formulario(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        edad = request.POST.get('edad')
        semestre = request.POST.get('semestre')
        promedio = request.POST.get('promedio')
        trabajo = request.POST.get('trabajo') == 'Sí'
        reprobado = request.POST.get('reprobado') == 'on'

        # Crear el estudiante
        student = Student.objects.create(
            nombre=nombre,
            edad=edad,
            semestre=semestre,
            promedio=promedio,
            trabajo=trabajo,
            reprobado=reprobado
        )

        # Lógica de riesgo (simulada para el ejemplo)
        if reprobado or float(promedio) < 50:
            riesgo = "Alto"
            probabilidad = random.randint(70, 100)
        elif float(promedio) < 70:
            riesgo = "Medio"
            probabilidad = random.randint(40, 69)
        else:
            riesgo = "Bajo"
            probabilidad = random.randint(10, 39)

        AnalysisResult.objects.create(
            student=student,
            edad=edad,
            semestre=semestre,
            promedio=promedio,
            trabajo=trabajo,
            reprobado=reprobado,
            riesgo=riesgo,
            probabilidad=probabilidad
        )

        return redirect('historial')

    return render(request, 'formulario.html')


# =========================================================
# HISTORIAL DE ANÁLISIS
# =========================================================
@login_required
def historial(request):
    registros = AnalysisResult.objects.select_related('student').all().order_by('-id')
    return render(request, 'historial.html', {'registros': registros})


# =========================================================
# CONSULTAS
# =========================================================
# =========================================================
# CONSULTAS
# =========================================================
@login_required
def consultas(request):
    # Recuperar parámetros del formulario
    nombre = request.GET.get('nombre', '').strip()
    semestre = request.GET.get('semestre', '').strip()
    fecha_inicio = request.GET.get('fecha_inicio', '')
    fecha_fin = request.GET.get('fecha_fin', '')

    # Base de datos inicial (con relación al estudiante)
    registros = AnalysisResult.objects.select_related('student').all().order_by('-id')

    # Filtros dinámicos
    if nombre:
        registros = registros.filter(student__nombre__icontains=nombre)
    if semestre:
        registros = registros.filter(semestre__icontains=semestre)
    if fecha_inicio:
        registros = registros.filter(fecha_registro__date__gte=fecha_inicio)
    if fecha_fin:
        registros = registros.filter(fecha_registro__date__lte=fecha_fin)

    # Renderizar con resultados filtrados
    return render(request, 'consultas.html', {'registros': registros})


# =========================================================
# REPORTES (exportaciones o tablas)
# =========================================================
@login_required
def reportes(request):
    estudiantes = AnalysisResult.objects.select_related('student').all().order_by('-id')
    return render(request, 'reportes.html', {'estudiantes': estudiantes})


# =========================================================
# DASHBOARD (con estadísticas visuales)
# =========================================================
@login_required
def dashboard(request):
    total_estudiantes = Student.objects.count()
    alto_riesgo = AnalysisResult.objects.filter(riesgo='Alto').count()
    medio_riesgo = AnalysisResult.objects.filter(riesgo='Medio').count()
    bajo_riesgo = AnalysisResult.objects.filter(riesgo='Bajo').count()

    # Simular precisión (puedes reemplazar con valor real si lo tienes)
    precision = 88

    # Simular tendencia temporal (últimos 7 días)
    fechas = []
    tendencia = []
    hoy = datetime.now()
    for i in range(7):
        dia = hoy - timedelta(days=6 - i)
        fechas.append(dia.strftime("%d/%m"))
        tendencia.append(random.randint(30, 95))

    context = {
        'total_estudiantes': total_estudiantes,
        'alto_riesgo': alto_riesgo,
        'medio': medio_riesgo,
        'bajo': bajo_riesgo,
        'precision': precision,
        'fechas': fechas,
        'tendencia': tendencia
    }

    return render(request, 'dashboard.html', context)

@login_required
def estadisticas(request):
    return render(request, 'estadisticas.html')

from django.http import HttpResponse
import csv
from .models import AnalysisResult  # Ajusta si tu modelo se llama diferente

@login_required
def export_studentrecords_csv(request):
    # Configura la respuesta HTTP como archivo CSV
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="resultados_desercion.csv"'

    writer = csv.writer(response)
    writer.writerow(['ID', 'Nombre', 'Edad', 'Semestre', 'Promedio', 'Trabajo', 'Reprobado', 'Riesgo', 'Probabilidad', 'Fecha'])

    registros = AnalysisResult.objects.all()

    for r in registros:
      writer.writerow([
        r.id,
        r.student.nombre if r.student else 'Sin nombre',
        r.edad,
        r.semestre,
        r.promedio,
        'Sí' if r.trabajo else 'No',
        'Sí' if r.reprobado else 'No',
        r.riesgo,
        f"{r.probabilidad}%",
        r.fecha_registro.strftime('%Y-%m-%d %H:%M'),
      ])

    return response

from openpyxl import Workbook
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import AnalysisResult

@login_required
def export_studentrecords_excel(request):
    # Crear un nuevo libro de Excel
    wb = Workbook()
    ws = wb.active
    ws.title = "Resultados de Deserción"

    # Escribir los encabezados
    ws.append(['ID', 'Nombre', 'Edad', 'Semestre', 'Promedio', 'Trabajo', 'Reprobado', 'Riesgo', 'Probabilidad', 'Fecha'])

    # Consultar los datos
    registros = AnalysisResult.objects.all()
    for r in registros:
      ws.append([
        r.id,
        r.student.nombre if r.student else 'Sin nombre',
        r.edad,
        r.semestre,
        r.promedio,
        'Sí' if r.trabajo else 'No',
        'Sí' if r.reprobado else 'No',
        r.riesgo,
        f"{r.probabilidad}%",
        r.fecha_registro.strftime('%Y-%m-%d %H:%M'),
      ])

    # Configurar la respuesta HTTP
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename="resultados_desercion.xlsx"'
    wb.save(response)
    return response

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("dashboard")  # Redirige al dashboard tras iniciar sesión
        else:
            messages.error(request, "Usuario o contraseña incorrectos")

    return render(request, "login.html")
from django.contrib.auth import logout

def logout_view(request):
    logout(request)
    return redirect('login')
