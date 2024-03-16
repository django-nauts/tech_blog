from django import forms
from blog.models import Post


class PostForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].label = 'Title'
        self.fields['body'].label = 'Main text'
        self.fields['cover'].label = 'Cover image'
        self.fields['categories'].label = 'Please select category'

    class Meta:
        model = Post
        fields = ['title', 'body', 'cover', 'categories']
        widgets = {
            'title': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'body': forms.Textarea(
                attrs={
                    'class': 'form-control'
                }
            ),
            'cover': forms.FileInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'categories': forms.SelectMultiple(
                attrs={
                    'class': 'form-control'
                }
            ),
        }


class UpdatePostForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].label = 'Title'
        self.fields['body'].label = 'Main text'
        self.fields['cover'].label = 'Cover image'
        self.fields['categories'].label = 'Please select category'

    class Meta:
        model = Post
        fields = ['title', 'body', 'cover', 'categories']
        widgets = {
            'title': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'body': forms.Textarea(
                attrs={
                    'class': 'form-control'
                }
            ),
            'cover': forms.FileInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'categories': forms.SelectMultiple(
                attrs={
                    'class': 'form-control'
                }
            ),
        }
