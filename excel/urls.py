from django.urls import path
from .views import CargarProductosView

urlpatterns = [
    path('cargar_productos/', CargarProductosView.as_view(), name='cargar_productos'),
]
