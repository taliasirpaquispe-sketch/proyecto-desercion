from django.db import models
from django.contrib.auth.models import User

class Semester(models.Model):
    number = models.PositiveSmallIntegerField(unique=True)
    name = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f"Semestre {self.number}"

class Student(models.Model):
    nombre = models.CharField(max_length=100)
    edad = models.IntegerField()
    semestre = models.CharField(max_length=20)   # sigue siendo CharField
    promedio = models.FloatField()
    trabajo = models.CharField(max_length=50)
    reprobado = models.BooleanField(default=False)
    riesgo = models.CharField(max_length=20, null=True, blank=True)
    probabilidad = models.FloatField(null=True, blank=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre

class AnalysisResult(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='analyses')
    edad = models.PositiveSmallIntegerField(null=True, blank=True)
    semestre = models.CharField(max_length=20, null=True, blank=True)  # CHAR para evitar duplicar semestres
    promedio = models.FloatField(null=True, blank=True)
    trabajo = models.BooleanField(null=True, blank=True)
    reprobado = models.BooleanField(null=True, blank=True)
    riesgo = models.CharField(max_length=20, null=True, blank=True)
    probabilidad = models.FloatField(null=True, blank=True)
    created_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student} - {self.riesgo}"
