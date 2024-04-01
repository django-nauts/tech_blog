from django.db import models
from django.utils import timezone
from django.template.defaultfilters import slugify
from django.urls import reverse
from taggit.managers import TaggableManager
from app_account.models import User


class PostPublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)


class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'
        WITHDRAWN = 'W', 'Withdrawn'

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_articles', blank=True, null=True)
    cover = models.ImageField(upload_to='images/', default='default.jpg')
    title = models.CharField(max_length=255, blank=False, null=False)
    slug = models.SlugField(blank=False, null=False, unique=True)
    body = models.TextField(blank=False, null=False)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2,
                              choices=Status.choices,
                              default=Status.PUBLISHED)
    likes = models.ManyToManyField(User, related_name='like', default=None, blank=True)
    likes_count = models.BigIntegerField(default='0')
    likes_plurality = models.CharField(max_length=10, blank=False, null=False, default='like')
    user_like = models.BooleanField(blank=True, default=False)
    bootstrap_class_name = models.CharField(max_length=20, blank=True, default="fa fa-heart-o")

    objects = models.Manager()  # The default manager
    published_posts = PostPublishedManager()  # The custom manager
    tags = TaggableManager()


    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish']),
        ]


    def __str__(self):
        return self.title


    def get_absolute_url(self):
        return reverse("blog_detail", kwargs={'slug': self.slug})


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)



class PostVisit(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    ip_address = models.CharField(max_length=30, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.post.title} - {self.ip_address}'


class Comment(models.Model):
    author = models.CharField(max_length=60)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey("Post", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.author} on '{self.post}'"
