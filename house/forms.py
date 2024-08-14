from django import forms


from .models import Post, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['category',
                  'title',
                  'text_post',
                  'upload'
                  ]
        labels = {
            'category': 'Категория',
            'title': 'Заголовок',
            'text_post': 'Текст',
            'upload': 'Файлы'
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('textPost',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'