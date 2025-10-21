from django.db import models

class StudentRecord(models.Model):
    edad = models.IntegerField()
    semestre = models.IntegerField()
    promedio = models.FloatField()
    trabajo = models.BooleanField()
    reprobado = models.BooleanField()
    riesgo = models.CharField(max_length=10)
    probabilidad = models.FloatField()
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Estudiante {self.id} - Riesgo: {self.riesgo}"
