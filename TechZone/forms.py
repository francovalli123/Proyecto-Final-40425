from django import forms
from django.forms import URLInput

class BuscarProductoForm(forms.Form):
    criterio_nombre = forms.CharField(max_length=100)


