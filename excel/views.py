from django.shortcuts import render
from django.views import View
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib import messages

from django.core.exceptions import ValidationError
from .models import Agenda, Service
import pandas as pd
import datetime


class AgendaUploadView(View):
    template_name = 'upload_excel.html'

    def get(self, request):
        return render(request, self.template_name)
    def post(self, request):
        # Verificar si se seleccionó un archivo
        excel_agenda = 'excel_file'
        if excel_agenda not in request.FILES:
            return render(request, self.template_name, {'error_message': 'Por favor, seleccione un archivo Excel para cargar'})
        # Si se seleccionó un archivo, continuar con la carga
        excel_file = request.FILES[excel_agenda]
        df = pd.read_excel(excel_file)
        # Convertir la columna 'dia' a datetime
        df['dia'] = pd.to_datetime(df['dia'], format='%d/%m/%Y')
        agendas = []
        errors = []
        # Procesar cada fila del archivo
        for index, row in df.iterrows():
            # Validar que el día sea un día hábil de la semana
            date = row['dia'].date()
            if date.weekday() >= 6:
                errors.append(f"El día '{row['dia']}' no es un día hábil de la semana.")
                continue
            try:
                service = Service.objects.get(tipo_cancha=row['tipo_cancha'], numeracion=row['numeracion'])
            except Service.DoesNotExist:
                errors.append(f"El tipo de cancha '{row['tipo_cancha']}' con numeración '{row['numeracion']}' no existe.")
                continue
            agenda = Agenda(
                service=service,
                dia=row['dia'],
                horario=row['horario'],
                user=request.user,
            )
            agendas.append(agenda)
        try:
            # Crear las agendas en la base de datos
            Agenda.objects.bulk_create(agendas)
            if errors:
                return render(request, self.template_name, {'error_message': errors})
            else:
                return render(request, self.template_name, {'success_message': {'message': 'Agendas cargadas exitosamente.'}})
        except Exception as e:
            # Si ocurre un error, manejarlo y mostrar un mensaje de error
            return render(request, self.template_name, {'error_message': str(e)})






class ServiceCreateView(CreateView):

    model = Service
    template_name = 'services/registro.html'
    fields = ['name','numercion']
    success_url = reverse_lazy('services:services_lista')
    
class ServiceListView(ListView):
    template_name = 'services/services_list.html'

    def get_queryset(self):
        return Service.objects.all().order_by('-pk')

class AgendaCreateView(CreateView):

    model = Agenda
    template_name = 'services/agenda_registro.html'
    fields = ['service', 'dia', 'horario']
    success_url = reverse_lazy('services:agenda_lista')
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
class AgendaListView(ListView):

    template_name = 'services/agenda_list.html'

    def get_queryset(self):
        return Agenda.objects.filter().order_by('-pk')
    



service_registro = ServiceCreateView.as_view()
agenda_registro = AgendaCreateView.as_view()

service_lista = ServiceListView.as_view()
agenda_lista = AgendaListView.as_view()