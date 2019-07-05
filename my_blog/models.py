from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

from taggit.managers import TaggableManager
from mdeditor.fields import MDTextField

# Create your models here.


class ArticleManager(models.Manager):
    def distinct_date(self):
        archive_list = []
        # .values 是把所有日期取出来
        for date in self.filter(status='published').values('publish'):
            # 上面取出来的值是 字典
            # 然后把日期格式化为 年月
            date = date['publish'].strftime('%Y%m')
            # 日期去重
            # 如果格式化后的日期不在列表中，则把它添加至列表中
            if date not in archive_list:
                archive_list.append(date)
        # 列表反转
        archive_list.sort(reverse=True)
        return archive_list


class Category(models.Model):
    name = models.CharField(max_length=64)


class Article(models.Model):
    STATUS_CHOICES = (('draft', 'Draft'), ('published', 'Published'))
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now())
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    tags = TaggableManager()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=None)
    objects = ArticleManager()

    class Meta:
        # verbose_name = "文章"
        ordering = ('-publish',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.publish.year, self.publish.month, self.publish.day, self.slug])


class Comment(models.Model):
    post = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=64)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ("created",)

    def __str__(self):
        return 'Comment by {} on {}'.format(self.name, self.post)
