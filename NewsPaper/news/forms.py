from django import forms
from django.core.exceptions import ValidationError
from .models import Post, Category, Author


class PostsForm(forms.ModelForm):
    text = forms.CharField(min_length=20, widget=forms.Textarea,
                           label='Текст поста')
    header = forms.CharField(widget=forms.Textarea, label='Заголовок поста')
    category = forms.ModelMultipleChoiceField(queryset=Category.objects.all(),
                                              label='Категории поста')
    author = forms.ModelChoiceField(queryset=Author.objects.all(),
                                              label='Автор поста')
    post_type = forms.CharField(widget=forms.HiddenInput())

    class Meta:
        model = Post
        fields = [
            'author',
            'category',
            'header',
            'text',
        ]


class NewsEditForm(forms.ModelForm):
    text = forms.CharField(min_length=20, widget=forms.Textarea,
                           label='Текст новости')
    header = forms.CharField(widget=forms.Textarea, label='Заголовок новости')
    category = forms.ModelMultipleChoiceField(queryset=Category.objects.all(),
                                              label='Категории новости')
    author = forms.ModelChoiceField(queryset=Author.objects.all(),
                                              label='Автор новости')
    post_type = forms.CharField(widget=forms.HiddenInput())

    class Meta:
        model = Post
        fields = [
            'author',
            'category',
            'header',
            'text',
            'post_type'
        ]

    def clean(self):
        cleaned_data = super().clean()
        post_type = cleaned_data.get("post_type")
        if post_type != 'N':
            raise ValidationError(
                "По этой ссылке вы можете редактировать только новость."
            )
        return cleaned_data


class ArticlesEditForm(forms.ModelForm):
    text = forms.CharField(min_length=20, widget=forms.Textarea,
                           label='Текст статьи')
    header = forms.CharField(widget=forms.Textarea,
                            label='Заголовок статьи')
    category = forms.ModelMultipleChoiceField(queryset=Category.objects.all(),
                                              label='Категории статьи')
    author = forms.ModelChoiceField(queryset=Author.objects.all(),
                                        label='Автор статьи')
    post_type = forms.CharField(widget=forms.HiddenInput())

    class Meta:
        model = Post
        fields = [
            'author',
            'category',
            'header',
            'text',
            'post_type'
        ]

    def clean(self):
        cleaned_data = super().clean()
        post_type = cleaned_data.get("post_type")
        if post_type != 'A':
            raise ValidationError(
                "По этой ссылке вы можете редактировать только новость."
            )
        return cleaned_data
