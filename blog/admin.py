from django.contrib import admin
from blog.models import Post, PostVisit


@admin.action(description="Mark selected stories as published")
def make_published(modeladmin, request, queryset):
    queryset.update(status="PB")

@admin.action(description="Mark selected stories as draft")
def make_draft(modeladmin, request, queryset):
    queryset.update(status="DF")

@admin.action(description="Mark selected stories as withdrawn")
def make_withdrawn(modeladmin, request, queryset):
    queryset.update(status="W")

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ['title', 'slug', 'author', 'publish', 'status']
    list_filter = ['status', 'created', 'publish', 'author']
    search_fields = ['title', 'body']
    raw_id_fields = ['author']
    date_hierarchy = 'publish'
    ordering = ['status', 'publish']
    actions = [make_published, make_draft, make_withdrawn]

    def save_model(self, request, obj, form, change):
        if not change:
            obj.author = request.user
        return super().save_model(request, obj, form, change)


admin.site.register(PostVisit)
