from django.shortcuts import render
from django.views.generic import ListView

from .models import Post, Category, Author, Comment


class HousePage(ListView):
    model = Post
    template_name = "housetemp/housepage.html"


def index(request):
    return render(request, template_name="housetemp/housepage.html")

