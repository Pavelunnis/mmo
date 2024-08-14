from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Post(models.Model):
    CAT = (('tank', 'танк'),
           ('healing', 'Хилы'),
           ('dd', 'ДД'),
           ('buy', 'Торговцы'),
           ('gild', 'Гилдмастеры'),
           ('quest', 'Квестгиверы'),
           ('smith', 'Кузнецы'),
           ('tanner', 'Кожевники'),
           ('potion', 'Зельевары'),
           ('spellmaster', 'Мастера заклинаний'),
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=128)
    text_post = models.TextField()
    category = models.CharField(max_length=18, choices=CAT, default='tank')
    upload = models.FileField(upload_to="uploads/", null=True, blank=True)
    time_in = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Объявление: {self.title}'

    def get_absolute_url(self):
        return reverse('postDetail', args=[str(self.id)])

    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'


class Comment(models.Model):
    commentPost = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    time_in = models.DateTimeField(auto_now_add=True)
    textPost = models.TextField()
    status = models.BooleanField(default=False)


    def __str__(self):
        return f'Пользователь {self.author} прокомментировал: {self.textPost}'



