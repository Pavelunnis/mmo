from django.contrib.auth.decorators import login_required
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.core.cache import cache
from django.shortcuts import redirect

from .models import Post, Comment
from .forms import PostForm, CommentForm
from .filters import PostFilter


class PostList(ListView):
    model = Post
    ordering = 'title'
    template_name = "houseTemp/housepage.html"
    context_object_name = 'Posts'
    paginate_by = 4

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context

class PostDetail(DetailView):
    model = Post
    template_name = 'houseTemp/Post.html'
    context_object_name = "Post"
    success_msg = 'Комментарий создан'

    def get_success_url(self):
        return reverse_lazy('postDetail', kwargs={'pk': self.get_object().id})

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.Post = self.get_object()
        self.object.author = self.request.user
        self.object.save()
        return super().form_valid(form)


class PostCreate(LoginRequiredMixin, CreateView):
    raise_exception = True
    form_class = PostForm
    model = Post
    template_name = 'houseTemp/post_create.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user
        post.save()
        return super().form_valid(form)


class PostUpdate(LoginRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'houseTemp/post_create.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.request.user != kwargs['instance'].author:
            return self.handle_no_permission()
        return kwargs


class CommentView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'houseTemp/Comment.html'
    success_url = "/posts"

    def form_valid(self, form):
        comment = form.save(commit= False)
        comment.author = self.request.user
        comment.commentPost_id = self.kwargs["pk"]
        return super().form_valid(form)


class UserResponseList(LoginRequiredMixin, ListView):
    model = Comment
    template_name = 'houseTemp/response.html'
    context_object_name = 'comments'
    paginate_by = 5

    def get_queryset(self):
        queryset = Comment.objects.filter(commentPost__author=self.request.user).all()
        return queryset

    def get_queryset(self):
        queryset = Comment.objects.filter(commentPost__author=self.request.user).order_by('-time_in').all()
        self.filterset = PostFilter(self.request.GET, queryset)
        self.filterset.form.fields['commentPost'].queryset = Post.objects.filter(author=self.request.user)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context

@login_required
def comments_accept(request, **kwargs):
    response = Comment.objects.get(id=kwargs.get('pk'))
    response.status = True
    response.save()
    return redirect(request.META.get('HTTP_REFERER'))


@login_required
def comments_delete(request, **kwargs):
    response = Comment.objects.get(id=kwargs.get('pk'))
    response.delete()
    return redirect(request.META.get('HTTP_REFERER'))