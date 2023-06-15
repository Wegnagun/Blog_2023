from django.shortcuts import render, get_object_or_404

from .models import Post


def post_list(request):  # представление списка постов
    posts = Post.published.all()
    return render(request, 'blog/list.html', {'posts': posts})


# детальное представление поста
def post_detail(request, year: int, month: int, day: int, post: str):
    post = get_object_or_404(
        Post,
        status=Post.Status.PUBLISHED,
        slug=post,
        publish__year=year,
        publish__month=month,
        publish__day=day
    )

    return render(request, 'blog/detail.html', {'post': post})
