from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count

from blog.models import Post
from blog.forms import PostForm, UpdatePostForm


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
            return redirect('blog_index')
    else:
        form = PostForm()

    context = {
        'form': form,
    }
    return render(request, 'blog/create.html', context)


# Home page
def blog_index(request):
    if request.method == 'GET':
        posts = Post.published_posts.all().order_by('-created')
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
        }
        return render(request, 'blog/tech-index.html', context)


# Show each post
def blog_detail(request, slug):
    post = Post.objects.get(slug=slug)

    # Show similar posts
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published_posts.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:2]

    context = {
        'post': post,
        'similar_posts': similar_posts,
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
        return redirect('blog_index')

    return render(request, 'blog/delete.html', context)


# Show author posts and information
def blog_author(request):
    context = {}
    return render(request, 'blog/tech-author.html', context)


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
        current_like_count = ''
        current_user_like = False
        current_like_plurality = ''
        post_id = int(request.POST.get('postid'))
        post = get_object_or_404(Post, id=post_id)

        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
            post.likes_count -= 1  # because the type of field is BigIntegerfield, its not necessary to check the number not to be less than zero
            current_like_count = post.likes_count
            if current_like_count > 1:
                post.likes_plurality = 'likes'
                current_like_plurality = post.likes_plurality
            else:
                post.likes_plurality = 'like'
                current_like_plurality = post.likes_plurality
            post.save()

        else:
            post.likes.add(request.user)
            post.likes_count += 1
            current_like_count = post.likes_count
            if current_like_count > 1:
                post.likes_plurality = 'likes'
                current_like_plurality = post.likes_plurality
            else:
                post.likes_plurality = 'like'
                current_like_plurality = post.likes_plurality
            post.user_like = True
            current_user_like = post.user_like
            post.save()

        print(current_like_count)
        print(current_like_plurality)
        print(current_user_like)

        return JsonResponse({
            'like_count': current_like_count,
            'user_like': current_user_like,
            'like_plurality': current_like_plurality,
        })


def footer_component(request):
    return render(request, 'shared/footer_component.html')


def header_component(request):
    return render(request, 'shared/header_component.html')
