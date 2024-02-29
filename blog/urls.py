from django.urls import path
from blog import views


urlpatterns = [
	path('', views.blog_index, name='blog_index'),
	path('<slug:slug>', views.blog_detail, name='blog_detail'),
	path('create/', views.blog_create, name='blog_create'),
	path('<slug:slug>/update/', views.blog_update, name='blog_update'),
	path('<slug:slug>/delete/', views.blog_delete, name='blog_delete'),
	path('category/<category>/', views.blog_category, name='blog_category'),
	path('category_01/', views.blog_category_01, name='blog_category_01'),
	path('category_02/', views.blog_category_02, name='blog_category_02'),
	path('category_03/', views.blog_category_03, name='blog_category_03'),
	path('author/', views.blog_author, name='blog_author'),
	path('contact/', views.blog_contact, name='blog_contact'),
]
