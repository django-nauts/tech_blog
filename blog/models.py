from django.db import models


class Category(models.Model):
	name = models.CharField(max_length=30)

	class Meta:
		verbose_name_plural = "categories"

	def __str__(self):
		return self.name



class Post(models.Model):
	cover = models.ImageField(upload_to="images/", default="default.jpg")
	title = models.CharField(max_length=255, blank=False, null=False)
	body = models.TextField(blank=False, null=False)
	created_on = models.DateTimeField(auto_now_add=True)
	last_modified = models.DateTimeField(auto_now=True)
	categories = models.ManyToManyField("Category", related_name="posts")

	def __str__(self):
		return self.title
