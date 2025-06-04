from django import forms
from .models import Poem


class PoemFilterForm(forms.Form):
    title = forms.CharField(required=False, label='Поиск по названию')
    year = forms.ChoiceField(required=False, label='Год')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        years = Poem.objects.values_list('year', flat=True).distinct().order_by('-year')
        self.fields['year'].choices = [('', 'Все годы')] + [(year, year) for year in years]