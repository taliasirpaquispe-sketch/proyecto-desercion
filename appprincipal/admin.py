from django.contrib import admin
from .models import Student, Semester, AnalysisResult

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'edad', 'semestre', 'promedio', 'riesgo', 'probabilidad', 'fecha_registro')
    search_fields = ('nombre',)
    list_filter = ('riesgo', 'semestre')

@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
    list_display = ('id', 'number', 'name')

@admin.register(AnalysisResult)
class AnalysisResultAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'edad', 'semestre', 'promedio', 'trabajo', 'reprobado', 'riesgo', 'probabilidad', 'fecha_registro')
    search_fields = ('student__nombre',)
    list_filter = ('riesgo', 'semestre')
