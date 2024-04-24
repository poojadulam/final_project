from django import forms
from .models import TableReservation

class TableReservationForm(forms.ModelForm):
    class Meta:
        model = TableReservation
        fields = ['date', 'time', 'number_of_people', 'status']
