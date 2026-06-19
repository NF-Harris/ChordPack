import  django_filters
from api.models import Chord

class ProductFilter(django_filters.FilterSet):
    class Meta:
        model = Chord
        fields = {"title":["icontains"],
"artist":["icontains"],
"content":["icontains"]}
