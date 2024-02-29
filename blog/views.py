from django.shortcuts import (
	render, redirect, get_object_or_404
)

from blog.models import Post
from blog.forms import PostForm, UpdatePostForm


# Show specific category
def blog_category(request, category):
	posts = Post.objects.filter(
		categories__name__contains=category
	).order_by('-created')
	
	context = {
		'category': category,
		'posts': posts,
	}
	return render(request, 'blog/tech-category.html', context)


# Create a new post
def blog_create(request):

	if request.method == 'POST':
		form = PostForm(request.POST, request.FILES)

		if form.is_valid():
			form.save()
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
		context = {
			'posts': posts,
		}
		return render(request, 'blog/tech-index.html', context)


# Show each post
def blog_detail(request, slug):
	post = Post.objects.get(slug=slug)
	context = {
		'post': post,
	}
	return render(request, 'blog/tech-single.html', context)


# Update post
def blog_update(request, slug):
	post = get_object_or_404(Post, slug=slug)

	if request.method == 'POST':
		form = UpdatePostForm(request.POST, request.FILES, instance=post)
		if form.is_valid():
			form.save()
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


def blog_category_01(request):
	context = {}
	return render(request, 'blog/tech-category-01.html', context)


def blog_category_02(request):
	context = {}
	return render(request, 'blog/tech-category-02.html', context)


def blog_category_03(request):
	context = {}
	return render(request, 'blog/tech-category-03.html', context)


# Contact us
def blog_contact(request):
	context = {}
	return render(request, 'blog/tech-contact.html', context)
