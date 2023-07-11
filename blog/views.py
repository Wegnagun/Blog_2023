from django.conf import settings
from django.core.mail import send_mail
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST
from taggit.models import Tag
from django.db.models import Count

from .forms import EmailPostForm, CommentForm
from .models import Post


def post_list(request, tag_slug=None):
    """ Представление списка постов. """
    post_list = Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        post_list = post_list.filter(tags__in=[tag])
    paginator = Paginator(post_list, settings.MAX_PAGES)
    page_number = request.GET.get('page', 1)
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    context = {'posts': posts, 'tag': tag}
    return render(request, 'blog/list.html', context)

# class PostListView(ListView, tag_slug=None):
#     """ Представление списка постов. """
#
#     queryset = Post.published.all()
#     context_object_name = 'posts'
#     paginate_by = settings.MAX_PAGES
#     template_name = 'blog/list.html'
#
#     def get_context_data(self, **kwargs):
#         try:
#             return super(PostListView, self).get_context_data(**kwargs)
#         except Http404:
#             self.kwargs['page'] = 1
#             return super(PostListView, self).get_context_data(**kwargs)


def post_detail(request, year: int, month: int, day: int, post: str):
    """ Детальное представление поста. """
    similar_posts_showing_count = 4
    post = get_object_or_404(
        Post,
        status=Post.Status.PUBLISHED,
        slug=post,
        publish__year=year,
        publish__month=month,
        publish__day=day
    )
    comments = post.comments.filter(active=True)
    form = CommentForm()
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(
        id=post.id
    ).annotate(same_tags=Count('tags')).order_by(
        '-same_tags', '-publish'
    )[:similar_posts_showing_count]
    context = {
        'post': post,
        'comments': comments,
        'form': form,
        'similar_posts': similar_posts
    }

    return render(request, 'blog/detail.html', context)


def post_share(request, post_id):
    """ Обработка формы предложки поста на почту. """

    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    sent = False
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} советуем прочитать {post.title}"
            message = f"Прочитайте {post.title} на {post_url}\n\n" \
                      f"{cd['name']}\'s прокомментировал: {cd['comments']}"
            send_mail(subject, message, 'wegnagun@bk.ru', [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    context = {
        'post': post,
        'form': form,
        'sent': sent
    }
    return render(request, 'blog/share.html', context)


@require_POST
def post_comment(request, post_id):
    """ Обработка формы комментариев. """

    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    comment = None
    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
    context = {
        'post': post,
        'form': form,
        'comment': comment
    }
    return render(request, 'blog/comment.html', context)
