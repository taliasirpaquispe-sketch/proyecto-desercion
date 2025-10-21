from django.shortcuts import render
import tensorflow as tf
import numpy as np
from .models import StudentRecord  # 👈 Importamos el modelo

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

from django.db.models import Count, Avg
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def estadisticas(request):
    # Contar registros por nivel de riesgo
    conteos = StudentRecord.objects.values('riesgo').annotate(total=Count('riesgo'))

    # Calcular promedio general de notas
    promedio_general = StudentRecord.objects.aggregate(promedio=Avg('promedio'))['promedio']

    # Preparar datos para Chart.js
    labels = [c['riesgo'] for c in conteos]
    data = [c['total'] for c in conteos]

    context = {
        'labels': labels,
        'data': data,
        'promedio_general': round(promedio_general, 2) if promedio_general else 0
    }

    return render(request, 'estadisticas.html', context)

# --- Página de login ---
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('historial')
        else:
            return render(request, 'login.html', {'error': 'Usuario o contraseña incorrectos'})
    return render(request, 'login.html')


# --- Cerrar sesión ---
def logout_view(request):
    logout(request)
    return redirect('login')


# --- Proteger historial ---
@login_required(login_url='login')
def historial(request):
    registros = StudentRecord.objects.all().order_by('-fecha_registro')
    return render(request, 'historial.html', {'registros': registros})

def historial(request):
    registros = StudentRecord.objects.all().order_by('-fecha_registro')
    return render(request, 'historial.html', {'registros': registros})
# --- Página de inicio ---
def inicio(request):
    return render(request, 'inicio.html')


# --- Página del formulario ---
def formulario(request):
    if request.method == 'POST':
        edad = int(request.POST['edad'])
        semestre = int(request.POST['semestre'])
        promedio = float(request.POST['promedio'])
        trabajo = 1 if request.POST['trabajo'] == 'si' else 0
        reprobado = 1 if request.POST['reprobado'] == 'si' else 0

        entrada = np.array([[edad / 60, semestre / 10, promedio / 100, trabajo, reprobado]])

        modelo = tf.keras.Sequential([
            tf.keras.layers.Dense(8, activation='relu', input_shape=(5,)),
            tf.keras.layers.Dense(4, activation='relu'),
            tf.keras.layers.Dense(1, activation='sigmoid')
        ])

        prediccion = modelo(entrada).numpy()[0][0]

        if prediccion > 0.66:
            riesgo = "ALTO"
        elif prediccion > 0.33:
            riesgo = "MEDIO"
        else:
            riesgo = "BAJO"

        probabilidad = round(float(prediccion) * 100, 2)

        # 👇 Guardamos el registro en la base
        StudentRecord.objects.create(
            edad=edad,
            semestre=semestre,
            promedio=promedio,
            trabajo=bool(trabajo),
            reprobado=bool(reprobado),
            riesgo=riesgo,
            probabilidad=probabilidad
        )

        return render(request, 'resultado.html', {
            'riesgo': riesgo,
            'probabilidad': probabilidad
        })

    return render(request, 'formulario.html')
