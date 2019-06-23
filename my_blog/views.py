from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Article, Comment
from .forms import CommentForm

from taggit.models import Tag

# Create your views here.


def article_list(request, tag_slug=None):
    # 获取所有文章
    # object_list = Article.objects.all()
    # 获取 status='published' 的文章，使用 filter 方法
    object_list = Article.objects.filter(status='published')
    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])

    paginator = Paginator(object_list, 5)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    # 获取所有标签
    tags = Article.tags.all()

    return render(request, 'blog/post/list.html', {'page': page, 'posts': posts, 'tag': tag, 'tags': tags})


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Article, slug=post, status="published", publish__year=year, publish__month=month,
                             publish__day=day)
    comments = post.comments.filter(active=True)

    new_comment = None

    if request.method == "POST":
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
    else:
        comment_form = CommentForm
    return render(request, 'blog/post/detail.html', {'post': post, 'comments': comments, 'new_comment': new_comment, 'comment_form': comment_form})


def about(request):
    return render(request, 'blog/about.html')


def search(request):
    query_set = set()
    if request.method == "GET":
        keyword = request.GET.get('keyword')
        # 判断 keyword 是否为空或者空格，是的话重定向到首页
        if not keyword or keyword.isspace():
            # redirect 重定向
            return redirect('/')
        else:
            object_list = Article.objects.filter(status="published")
            # 查询 title，使用 title__icontains ,意为查询 title 中是否含有 keyword，大小写不敏感
            for i in object_list.filter(title__icontains=keyword):
                query_set.add(i)
            # 查询 body
            for i in object_list.filter(body__icontains=keyword):
                query_set.add(i)
            # 后期可以搞下分页
    return render(request, 'blog/search.html', {'posts': query_set})
