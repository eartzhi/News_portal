from django_filters import FilterSet, ModelChoiceFilter, DateTimeFilter, \
  DateFilter, CharFilter, ChoiceFilter
from .models import Post, Author
from django.forms import DateInput, DateTimeInput


class PostsFilter(FilterSet):
    author = ModelChoiceFilter(
        field_name='author',
        queryset=Author.objects.all(),
        label='Автор статьи',
        empty_label='любой'
    )

    post_type = ChoiceFilter(
        field_name='post_type',
        label='Тип статьи',
        empty_label='любой',
        choices=Post.POST_TYPE_CHOISE
    )

    from_creation_time = DateTimeFilter(
        field_name='creation_time',
        label='С даты',
        lookup_expr='gte',
        widget=DateTimeInput(attrs={'type': 'date'})
    )

    to_creation_time = DateFilter(
        field_name='creation_time',
        label='До даты',
        lookup_expr='lte',
        widget=DateTimeInput(attrs={'type': 'date'})
    )

    text = CharFilter(
        field_name='text',
        label='Текст статьи содержит',
        lookup_expr='icontains',
    )

    header = CharFilter(
        field_name='header',
        label='Заголовок содержит',
        lookup_expr='icontains',
    )

    class Meta:
        model = Post
        fields = [
            'text',
            'header',
            'author',
            'post_type',
            'from_creation_time',
            'to_creation_time'
        ]
