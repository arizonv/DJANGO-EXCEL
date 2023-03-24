from datetime import date
from django.db import models
from django.conf import settings
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.db.models.fields.related import ForeignKey


class Service(models.Model):
    tipo_cancha = models.CharField(verbose_name="Name", max_length=30)
    NUMERCION_CANCHA = (
        ("1", "1"),
        ("2", "2"),
        ("3", "3"),
    )
    numeracion = models.CharField(verbose_name="Cancha",max_length=10, choices=NUMERCION_CANCHA)
    
    def __str__(self):
        return f'{self.tipo_cancha}  ;   C.0{self.numeracion}  '

def validar_dia(value):
    today = date.today()
    weekday = date.fromisoformat(f'{value}').weekday()

    if value < today:
        raise ValidationError('No se puede elegir una fecha pasada')
    if (weekday == 5) or (weekday == 6):
        raise ValidationError('escoja un dia habil de la semana.')

from django.core.exceptions import ValidationError



class Agenda(models.Model):
    service = ForeignKey(Service, on_delete=models.CASCADE, related_name='agenda')
    dia = models.DateField(help_text="Ingresa datos para agenda", validators=[validar_dia])
    HORARIOS_AM = (
        ("09", "09:00 AM"),
        ("10", "10:00 AM"),
        ("11", "11:00 AM"),
        ("12", "12:00 PM"),
    )

    HORARIOS_PM = (
        ("17", "05:00 PM"),
        ("18", "06:00 PM"),
        ("19", "07:00 PM"),
        ("20", "08:00 PM"),
        ("21", "09:00 PM"),
        ("22", "10:00 PM"),
    )

    horario = models.CharField(max_length=10, choices=HORARIOS_AM + (("", ""),) + HORARIOS_PM)

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        verbose_name='Usuario', 
        on_delete=models.CASCADE
    )

    def clean(self):
        if self.horario == "":
            raise ValidationError("Debe seleccionar un horario válido")
    
    class Meta:
        unique_together = ('dia','horario','service')
        
    def __str__(self):
        return f'{self.dia.strftime("%b %d %Y")} - {self.get_horario_display()} - {self.service}'