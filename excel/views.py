from django.shortcuts import render
import pandas as pd
from django.http import HttpResponse
from .models import Producto
from django.views import View


from django.core.exceptions import ValidationError

class CargarProductosView(View):
    def get(self, request):
        return render(request, 'register.html')
    
    def post(self, request):
        excel_file = request.FILES["excel_file"]
        
        # Leer el archivo Excel con Pandas
        df = pd.read_excel(excel_file)
        
        # Iterar sobre las filas del DataFrame
        for index, row in df.iterrows():
            nombre = row['nombre']
            descripcion = row['descripcion']
            precio = row['precio']
            stock = row['stock']
            
            # Validar los datos
            try:
                if not nombre or not descripcion or not precio or not stock:
                    raise ValidationError("Todos los campos son requeridos")
                
                precio = float(precio)
                if precio <= 0:
                    raise ValidationError("El precio debe ser mayor que cero")
                
                stock = int(stock)
                if stock < 0:
                    raise ValidationError("El stock no puede ser negativo")
            except ValidationError as e:
                # Si hay un error de validación, agregar el error al diccionario de errores del formulario y continuar con la siguiente fila
                form.add_error(None, e)
                continue
            
            # Crear un objeto Producto para cada fila
            producto = Producto(nombre=nombre, descripcion=descripcion, precio=precio, stock=stock)
            producto.save()
        
        return HttpResponse("Productos cargados correctamente")

