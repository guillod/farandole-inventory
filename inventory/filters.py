from django_filters import FilterSet, ModelChoiceFilter

from .models import Object

class ObjectFilter(FilterSet):

    #state = ModelChoiceFilter(queryset=Object.objects.all(), empty_label='Nationality')

    class Meta:
        model = Object
        fields = ['group', 'location', 'state']
