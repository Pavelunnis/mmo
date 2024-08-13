from django import forms
from .models import Post, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title_name', 'text_post', 'category', 'upload', ]
        widgets = {'author': forms.HiddenInput()}


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['textPost',]
        widgets = {'commentUser': forms.HiddenInput()}

class UserCommentAcceptForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = []
        widgets = {'commentUser': forms.HiddenInput()}