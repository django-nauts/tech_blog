from django.urls import path
from blog import views


urlpatterns = [
	path("", views.blog_index, name="blog_index"),
	path("post/<int:pk>/", views.blog_detail, name="blog_detail"),
	path("create/", views.blog_create, name="blog_create"),
	path("post/<int:pk>/update/", views.blog_update, name="blog_update"),
	path("post/<int:pk>/delete/", views.blog_delete, name="blog_delete"),
	path("category/<category>/", views.blog_category, name="blog_category"),
]
