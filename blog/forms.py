from django import forms
from blog.models import Post


class PostForm(forms.ModelForm):
	class Meta:
		model = Post
		fields = ['author', 'cover', 'title', 'body', 'categories']


class UpdatePostForm(forms.ModelForm):
	class Meta:
		model = Post
		fields = ['author', 'cover', 'title', 'slug', 'body', 'categories']
