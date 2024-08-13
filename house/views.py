
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.core.cache import cache
from django.shortcuts import redirect

from .models import Post, Comment
from .forms import PostForm, CommentForm, UserCommentAcceptForm
from .filters import PostFilter

class HousePage(ListView):
    model = Post
    ordering = 'title_name'
    template_name = "housetemp/housepage.html"
    context_object_name = 'Posts'


class PostDetail(DetailView):
    model = Post
    template_name = 'housetemp/Post.html'
    context_object_name = "Post"

    def get_object(self, *args, **kwargs):
        obj = cache.get(f'post-{self.kwargs["pk"]}',
                        None)
        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'post-{self.kwargs["pk"]}', obj)
            return obj


class PostCreate(LoginRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = 'housetemp/post_edit.html'
    success_url = "/posts"

    def form_valid(self, form):
        post = form.save(commit = False)
        post.author = self.request.user
        post.save()
        return super().form_valid(form)


class PostUpdate(LoginRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'housetemp/post_edit.html'


class CommentView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'housetemp/Comment.html'
    success_url = "/posts"

    def form_valid(self, form):
        comment = form.save(commit= False)
        comment.commentUser = self.request.user
        comment.commentPost_id = self.kwargs["pk"]
        return super().form_valid(form)

class UserResponseList(LoginRequiredMixin, ListView):
    model = Comment
    template_name = 'housetemp/response.html'
    context_object_name = 'comments'
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        # Добавляем в контекст объект фильтрации.
        context['filterset'] = self.filterset
        return context

class UserResponseDelete(LoginRequiredMixin, DeleteView):
    raise_exception = True
    model = UserCommentAcceptForm
    template_name = 'housetemp/response_delete.html'
    success_url = reverse_lazy('response')


class UserResponseAccept(LoginRequiredMixin, UpdateView):
    raise_exception = True
    form_class = UserCommentAcceptForm
    model = CommentForm
    template_name = 'housetemp/response_edit.html'
    success_url = reverse_lazy('response')

    def post(self, request, pk, **kwargs):
        if request.method == 'POST':
            Comment = CommentForm.objects.get(id=pk)
            Comment.status = True
            Comment.save()
            return redirect(f'response')
        else:
            return redirect(f'response')