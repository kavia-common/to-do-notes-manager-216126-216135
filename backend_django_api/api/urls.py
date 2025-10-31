from django.urls import path
from .views import health, notes_collection, notes_detail

urlpatterns = [
    path('health/', health, name='Health'),
    # Notes endpoints
    path('notes/', notes_collection, name='notes-list-create'),
    path('notes/<int:id>/', notes_detail, name='notes-detail'),
]
