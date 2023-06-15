from django.shortcuts import render, get_object_or_404

from .models import Post


def post_list(request):  # представление списка постов
    posts = Post.published.all()
    return render(request, 'blog/list.html', {'posts': posts})


def post_detail(request, id: int):  # детальное представление поста
    post = get_object_or_404(Post, pk=id, status=Post.Status.PUBLISHED)

    return render(request, 'blog/detail.html', {'post': post})
