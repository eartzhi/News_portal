from datetime import timedelta

import django_filters
from django.contrib.auth.mixins import LoginRequiredMixin, \
    PermissionRequiredMixin
from django.http import HttpResponseForbidden, HttpResponse, Http404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, \
    DeleteView, View
from .models import Post, Category, Author
from .filters import PostsFilter
from .forms import PostsForm, NewsEditForm, ArticlesEditForm, AccountForm
from django.urls import reverse_lazy
from django.contrib.auth.models import Group, User
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from .tasks import post_create_notify
from django.utils import timezone
from django.core.cache import cache
from django.utils.translation import gettext
import pytz
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import permissions

from .serializers import *
from .models import *

class PostList(ListView):
    model = Post
    ordering = 'creation_time'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 2

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.\
            filter(name='authors').exists()
        return context

    # def get(self, request):
    #     curent_time = timezone.now()
    #
    #     context = {
    #         'current_time': timezone.now(),
    #         'timezones': pytz.common_timezones
    #         # добавляем в контекст все доступные часовые пояса
    #     }
    #
    #     return HttpResponse(render(request, 'posts.html', context))
    #
    # #  по пост-запросу будем добавлять в сессию часовой пояс, который и будет обрабатываться написанным нами ранее middleware
    # def post(self, request):
    #     request.session['django_timezone'] = request.POST['timezone']
    #     return redirect('/posts/')


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.\
            filter(name='authors').exists()
        return context

    def get_object(self, *args, **kwargs):
        obj = cache.get(f'post-{self.kwargs["pk"]}', None)
        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'post-{self.kwargs["pk"]}', obj)
        return obj


class SearchPost(ListView):
    model = Post
    ordering = 'creation_time'
    template_name = 'search.html'
    context_object_name = 'posts'

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostsFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class NewsCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post', )
    form_class = PostsForm
    model = Post
    template_name = 'create_form.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.post_type = 'N'
        categories = list(set(form.cleaned_data['category'].values_list('category',
                                                                   flat=True)))
        post_create_notify.apply_async([categories, post.text, post.header],
                                       eta=timezone.now() + timedelta(seconds=10))
        return super().form_valid(form)


class ArticlesCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post', )
    form_class = PostsForm
    model = Post
    template_name = 'create_form.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.post_type = 'A'
        categories = list(set(form.cleaned_data['category'].values_list('category',
                                                                   flat=True)))
        post_create_notify.apply_async([categories, post.text, post.header],
                                       eta=timezone.now() + timedelta(seconds=10))
        return super().form_valid(form)


class NewsEdit(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post', )
    form_class = NewsEditForm
    model = Post
    template_name = 'update_form.html'


class ArticlesEdit(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post', )
    form_class = ArticlesEditForm
    model = Post
    template_name = 'update_form.html'


class NewsDelete(DeleteView):
    model = Post
    template_name = 'delete_form.html'
    success_url = reverse_lazy('posts_list')

    def form_valid(self, form):
        post = self.get_object()
        if post.post_type != 'N':
            return HttpResponseForbidden(
                gettext(
                "По этой ссылке вы можете удалить только новость"
                )
            )
        else:
            return super().form_valid(form)


class ArticlesDelete(DeleteView):
    model = Post
    template_name = 'delete_form.html'
    success_url = reverse_lazy('posts_list')

    def form_valid(self, form):
        post = self.get_object()
        if post.post_type != 'A':
            return HttpResponseForbidden(
                gettext(
                "По этой ссылке вы можете удалить только статью"
                )
            )
        else:
            return super().form_valid(form)


@login_required
def upgrade_me(request):
    user = request.user
    premium_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        premium_group.user_set.add(user)
        Author.objects.create(nick_name=user.username, user=user)
    return redirect('/posts')


class Account(LoginRequiredMixin, UpdateView):
    form_class = AccountForm
    model = User
    template_name = 'account_form.html'
    context_object_name = 'user'

    def get_object(self, *args, **kwargs):
        obj = super(Account, self).get_object(*args, **kwargs)
        if not obj.id == self.request.user.id:
            raise Http404
        return obj


# class Subscription(LoginRequiredMixin, UpdateView):
#     form_class = SubscriptionForm
#     model = Category
#     template_name = 'account_form.html'


class Subscription(ListView):
    model = Category
    ordering = 'category'
    template_name = 'categories.html'
    context_object_name = 'categories'
    paginate_by = 5


@login_required
def subscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscriber.add(user)
    return redirect('/posts/user/subscribe')


@login_required
def unsubscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscriber.remove(user)
    return redirect('/posts/user/subscribe')


# class IndexView(View):
#     def get(self, request):
#         printer.apply_async([10],
#                             eta=timezone.now() + timedelta(seconds=5))
#         hello.delay()
#         return HttpResponse('Hello!')


class NewsViewset(viewsets.ModelViewSet):
    queryset = Post.objects.filter(post_type='N').all()
    serializer_class = PostSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ["category", "author",]

    # def list(self, request):
    #     permission_classes = [permissions.AllowAny]
    #     return super().list(request)

    # def create(self, request):
    #     permission_classes = [permissions.IsAuthenticated]
    #     return super().create(request)
    #
    # def partial_update(self, request):
    #     permission_classes = [permissions.IsAuthenticated]
    #     return super().put(request)
    #
    # def destroy(self, request):
    #     permission_classes = [permissions.IsAuthenticated]
    #     return super().delete(request)


class ArticleViewset(viewsets.ModelViewSet):
    queryset = Post.objects.filter(post_type='A').all()
    serializer_class = PostSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ["category", "author"]

