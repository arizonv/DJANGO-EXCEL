from django.contrib import admin
from .models import Service, Agenda

class ServiceAdmin(admin.ModelAdmin):
    list_display = [
        'tipo_cancha', 'numeracion'
    ]


class AgendaAdmin(admin.ModelAdmin):
    list_display = [
        'dia', 'service', 'horario'
    ]
    

admin.site.register(Service,ServiceAdmin)
admin.site.register(Agenda, AgendaAdmin)