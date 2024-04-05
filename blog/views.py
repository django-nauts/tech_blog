from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count

from django.contrib import messages

from blog.models import Post, PostVisit, Comment
from blog.forms import PostForm, UpdatePostForm, CommentForm

from utils.http_service import get_client_ip


# Show specific category
def blog_category(request, tag):
    posts = Post.objects.filter(
        tags__name__contains=tag
    ).order_by('-created')

    paginator = Paginator(posts, 10)
    page_number = request.GET.get("page")

    # Display the last result instead of non-existing page.
    try:
        page_obj = paginator.get_page(page_number)
    except EmptyPage:
        page_obj = paginator.get_page(paginator.num_pages)

    # Display the first page in the page number is a character.
    except PageNotAnInteger:
        page_obj = paginator.page(1)

    context = {
        'tag': tag,
        'posts': posts,
        'page_obj': page_obj,
        }
    return render(request, 'blog/tech-category.html', context)


# Create a new post
def blog_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)

        if form.is_valid():
            obj = form.save(commit=False)
            obj.author = request.user
            obj.save()
            messages.success(request, 'Your post was created successfully!')
            return redirect('blog_index')
    else:
        form = PostForm()

    context = {
        'form': form,
    }
    return render(request, 'blog/create.html', context)


# Home page
def blog_index(request):

    favorite_posts = Post.objects.all().annotate(favorite_count=Count('likes')).order_by('-favorite_count','created')[:2]

    if request.method == 'GET':
        posts = Post.published_posts.all().order_by('-created').annotate(visit_count=Count('postvisit__ip_address'))
        paginator = Paginator(posts, 10)

        page_number = request.GET.get("page")

        # Display the last result instead of non-existing page.
        try:
            page_obj = paginator.get_page(page_number)
        except EmptyPage:
            page_obj = paginator.get_page(paginator.num_pages)

        # Display the first page in the page number is a character.
        except PageNotAnInteger:
            page_obj = paginator.page(1)

        context = {
            'posts': posts,
            'page_obj': page_obj,
            'favorite_posts': favorite_posts,
        }
        return render(request, 'blog/tech-index.html', context)


# Show each post
def blog_detail(request, slug):
    post = Post.objects.prefetch_related('postvisit_set').get(slug=slug)
    comments = Comment.objects.filter(post=post)

    form = CommentForm()
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = Comment(
                author=form.cleaned_data.get('author'),
                body=form.cleaned_data.get('body'),
                post=post,
            )
            comment.save()
            messages.success(request, 'Your comment was created successfully!', \
                             extra_tags='my_comment')
            return HttpResponseRedirect(request.path_info)

    # Show similar posts
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published_posts.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:2]

    # Get the previous and next posts based on the publish date
    previous_post = Post.objects.filter(publish__lt=post.publish).order_by('-publish').first()
    next_post = Post.objects.filter(publish__gt=post.publish).order_by('publish').first()

    # Get IP of each client and add it to db
    # Show the qunatity of post'visit
    user_ip = get_client_ip(request)
    user_id = None
    if request.user.is_authenticated:
        user_id = request.user
    user_is_visited = PostVisit.objects.filter(ip_address=user_ip, user=user_id, post=post.id).exists()
    if not user_is_visited:
        new_visit = PostVisit(ip_address=user_ip, post=post, user=request.user)
        new_visit.save()

    context = {
        'post': post,
        'similar_posts': similar_posts,
        'previous_post': previous_post,
        'next_post': next_post,
        'comments': comments,
        'form': CommentForm(),
    }
    return render(request, 'blog/tech-single.html', context)


# Update post
def blog_update(request, slug):
    post = get_object_or_404(Post, slug=slug)

    if request.method == 'POST':
        form = UpdatePostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.author = request.user
            obj.save()
            messages.success(request, 'Your post was updated successfully!')          
            return redirect('blog_index')
    else:
        form = UpdatePostForm(instance=post)

    context = {
        'post': post,
        'form': form,
    }
    return render(request, 'blog/update.html', context)


# Delete post
def blog_delete(request, slug):
    context = {}
    post = get_object_or_404(Post, slug=slug)

    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Your post was deleted successfully!')
        return redirect('blog_index')

    return render(request, 'blog/delete.html', context)


def blog_category_02(request):
    context = {}
    return render(request, 'blog/tech-category-02.html', context)


# Contact us
def blog_contact(request):
    context = {}
    return render(request, 'blog/tech-contact.html', context)


# Like a post by ajax
def like_post(request):
    if request.POST.get('action') == 'post':
        post_id = int(request.POST.get('postid'))
        like_action = request.POST.get('likeAction')

        if post_id and like_action:
            try:
                post = Post.objects.get(id=post_id)
                if like_action == "like":
                    post.likes.add(request.user)
                else:
                    post.likes.remove(request.user)
                return JsonResponse({'status': 'ok'})
            except Post.DoesNotExist:
                return JsonResponse({'status': 'error'})
        return JsonResponse({'status': 'error'})


def footer_component(request):
    return render(request, 'shared/footer_component.html')


def header_component(request):
    return render(request, 'shared/header_component.html')


def sidebar_component(request):
    # Sorting posts based on which ones have a more likes by clients
    favorite_posts = Post.objects.all().annotate(favorite_count=Count('likes')).order_by('-favorite_count','created')[:4]
    latest_comments = Comment.objects.order_by('-created_on')[:3]

    context = {
        'favorite_posts': favorite_posts,
        'latest_comments': latest_comments,
    }
    return render(request, 'shared/sidebar_component.html', context)
