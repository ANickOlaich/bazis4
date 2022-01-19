from django.shortcuts import render
from django.utils import timezone
from .models import Post

def post_list(request):
    posts = Post.objects.all
    return render(request, 'bazis/post_list.html', {'posts': posts})

def about(request):
    return render(request, 'bazis/about.html')
