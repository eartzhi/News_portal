from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden
from django.views.generic import ListView, DetailView, CreateView, UpdateView, \
    DeleteView
from .models import Post
from .filters import PostsFilter
from .forms import PostsForm, NewsEditForm, ArticlesEditForm
from django.urls import reverse_lazy
from django.core.exceptions import ValidationError
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect


class PostList(ListView):
    model = Post
    ordering = 'creation_time'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 2

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.\
            filter(name = 'authors').exists()
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'


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


class NewsCreate(CreateView):
    form_class = PostsForm
    model = Post
    template_name = 'create_form.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.post_type = 'N'
        return super().form_valid(form)


class ArticlesCreate(CreateView):
    form_class = PostsForm
    model = Post
    template_name = 'create_form.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.post_type = 'A'
        return super().form_valid(form)


class NewsEdit(LoginRequiredMixin, UpdateView):
    form_class = NewsEditForm
    model = Post
    template_name = 'update_form.html'


class ArticlesEdit(LoginRequiredMixin, UpdateView):
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
                "По этой ссылке вы можете удалить только новость"
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
                "По этой ссылке вы можете удалить только статью"
            )
        else:
            return super().form_valid(form)


@login_required
def upgrade_me(request):
    user = request.user
    premium_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        premium_group.user_set.add(user)
    return redirect('/posts')
