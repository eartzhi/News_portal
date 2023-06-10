from django import forms
from django.core.exceptions import ValidationError
from .models import Post, Category, Author
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group, User


class PostsForm(forms.ModelForm):
    text = forms.CharField(min_length=20, widget=forms.Textarea,
                           label='Текст поста')
    header = forms.CharField(widget=forms.Textarea, label='Заголовок поста')
    category = forms.ModelMultipleChoiceField(queryset=Category.objects.all(),
                                              label='Категории поста')
    author = forms.ModelChoiceField(queryset=Author.objects.all(),
                                    label='Автор поста')

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
                "По этой ссылке вы можете редактировать только статью."
            )
        return cleaned_data


class BasicSignupForm(SignupForm):

    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        common_group = Group.objects.get(name='common')
        common_group.user_set.add(user)
        return user


class AccountForm(forms.ModelForm):
    username = forms.CharField(max_length=150, widget=forms.TextInput,
                               label='Пользователь')
    first_name = forms.CharField(max_length=150, widget=forms.TextInput,
                                 label='Имя', required=False)
    last_name = forms.CharField(max_length=150, widget=forms.TextInput,
                                label='Фамилия', required=False)
    category = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(), widget=forms.CheckboxSelectMultiple,
        label='Подписка на категории', required=False)

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'category',
        ]


# class SubscriptionForm(forms.ModelForm):
#     subscriber = forms.ModelMultipleChoiceField(
#         queryset=Category.objects.all(), widget=forms.CheckboxSelectMultiple,
#         label='Подписка на категории', required=False)
#
#     class Meta:
#         model = Category
#         fields = [
#             'subscriber',
#         ]
