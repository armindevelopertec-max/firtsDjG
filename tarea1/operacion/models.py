from django.db import models

class Operacion(models.Model):
    numero1 = models.FloatField()
    numero2 = models.FloatField()
    resultado = models.FloatField()
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.numero1} + {self.numero2} = {self.resultado}"
