from django.urls import path
from .views import AgendaUploadView

urlpatterns = [
    path('register/', AgendaUploadView.as_view(), name='agendar'),
]
