from django import forms
from .models import Application, Hostel, Room

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['preferred_room', 'note']


class HostelForm(forms.ModelForm):
    class Meta:
        model = Hostel
        fields = ['name', 'location', 'capacity', 'description']


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['hostel', 'number', 'capacity', 'is_active']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
