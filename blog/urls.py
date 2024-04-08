from django.urls import path
from blog import views


urlpatterns = [
	path('', views.blog_index, name='blog_index'),
	path('<slug:slug>', views.blog_detail, name='blog_detail'),
	path('create/', views.blog_create, name='blog_create'),
	path('<slug:slug>/update/', views.blog_update, name='blog_update'),
	path('<slug:slug>/delete/', views.blog_delete, name='blog_delete'),
	path('category/<tag>/', views.blog_category, name='blog_category'),
	path('category_02/', views.blog_category_02, name='blog_category_02'),
	path('contact/', views.blog_contact, name='blog_contact'),
	path('like-post/',views.like_post, name='like_post'),
	path('user-comment/', views.user_comment, name='user_comment_page'),

]
