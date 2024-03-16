from django.db import models
from django.utils import timezone
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.contrib.contenttypes.fields import GenericRelation
from comment.models import Comment
from taggit.managers import TaggableManager

from account.models import User


class PostPublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)


class Post(models.Model):

    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_articles', blank=True, null=True)
    cover = models.ImageField(upload_to='images/', default='default.jpg')
    title = models.CharField(max_length=255, blank=False, null=False)
    slug = models.SlugField(blank=False, null=False, unique=True)
    body = models.TextField(blank=False, null=False)
    comments = GenericRelation(Comment)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2,
                             choices=Status.choices,
                             default=Status.DRAFT)
    objects = models.Manager() #The default manager
    published_posts = PostPublishedManager() #The custom manager
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
