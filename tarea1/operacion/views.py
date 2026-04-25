from django.shortcuts import render
from .models import Operacion

def suma(request):
    resultado = None
    n1 = None
    n2 = None
    
    if request.method == "POST":
        try:
            n1 = float(request.POST.get("num1", 0))
            n2 = float(request.POST.get("num2", 0))
            resultado = n1 + n2
            
            # Guardar en MariaDB
            Operacion.objects.create(numero1=n1, numero2=n2, resultado=resultado)
        except ValueError:
            resultado = "Error: Ingrese números válidos"

    # Obtener el historial
    historial = Operacion.objects.all().order_by('-fecha')[:5]

    return render(request, "operacion/suma.html", {
        "resultado": resultado,
        "n1": n1,
        "n2": n2,
        "historial": historial
    })
