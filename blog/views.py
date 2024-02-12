from django.shortcuts import (
	render, redirect, get_object_or_404
)

from blog.models import Post
from blog.forms import PostForm


# Show specific category
def blog_category(request, category):
	posts = Post.objects.filter(
		categories__name__contains=category
	).order_by("-created_on")
	
	context = {
		"category": category,
		"posts": posts,
	}
	return render(request, "blog/tech-category.html", context)


# Create a new post
def blog_create(request):
	form = PostForm(request.POST or None)
	
	if form.is_valid():
		form.save()
		return redirect('blog_index')

	context = {
		"form": form,
	}
	return render(request, "blog/create.html", context)


# Home page
def blog_index(request):
	posts = Post.objects.all().order_by("-created_on")
	context = {
		"posts": posts,
	}
	return render(request, "blog/tech-index.html", context)


# Show each post
def blog_detail(request, pk):
	post = Post.objects.get(pk=pk)
	context = {
		"post": post,
	}
	return render(request, "blog/tech-single.html", context)


# Update post
def blog_update(request, pk):
	post = get_object_or_404(Post, pk=pk)
	form = PostForm(request.POST or None, instance=post)

	if form.is_valid():
		form.save()
		return redirect("/post/" + str(pk))
	
	context = {
		"post": post,
		"form": form,
	}
	return render(request, "blog/update.html", context)


# Delete post
def blog_delete(request, pk):
	context = {}
	post = get_object_or_404(Post, pk=pk)

	if request.method == "POST":
		post.delete()
		return redirect('blog_index')

	return render(request, "blog/delete.html", context)


# Show author posts and information
def blog_author(request):
	context = {}
	return render(request, "blog/tech-author.html", context)


def blog_category_01(request):
	context = {}
	return render(request, "blog/tech-category-01.html", context)


def blog_category_02(request):
	context = {}
	return render(request, "blog/tech-category-02.html", context)


def blog_category_03(request):
	context = {}
	return render(request, "blog/tech-category-03.html", context)


# Contact us
def blog_contact(request):
	context = {}
	return render(request, "blog/tech-contact.html", context)
