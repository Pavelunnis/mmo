from django_filters import FilterSet
from .models import Comment


class PostFilter(FilterSet):
    class Meta:
        model = Comment
        fields = {
            'commentPost': ['exact'],
       }
