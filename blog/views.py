from django.shortcuts import (
	render, redirect, get_object_or_404
)

from blog.models import Post
from blog.forms import PostForm


def blog_category(request, category):
	posts = Post.objects.filter(
		categories__name__contains=category
	).order_by("-created_on")
	
	context = {
		"category": category,
		"posts": posts,
	}
	return render(request, "blog/category.html", context)


def blog_create(request):
	form = PostForm(request.POST or None)
	
	if form.is_valid():
		form.save()
		return redirect('blog_index')

	context = {
		"form": form,
	}
	return render(request, "blog/create.html", context)


def blog_index(request):
	posts = Post.objects.all().order_by("-created_on")
	context = {
		"posts": posts,
	}
	return render(request, "blog/index.html", context)


def blog_detail(request, pk):
	post = Post.objects.get(pk=pk)
	context = {
		"post": post,
	}
	return render(request, "blog/detail.html", context)


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


def blog_delete(request, pk):
	context = {}
	post = get_object_or_404(Post, pk=pk)

	if request.method == "POST":
		post.delete()
		return redirect('blog_index')

	return render(request, "blog/delete.html", context)
