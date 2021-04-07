from django.contrib import admin, messages
from django.utils.translation import ngettext
from .models import Article, Category

# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('position', 'title', 'slug', 'parent', 'status')
    list_filter = (['status'])
    search_fields = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}
    actions = ['make_status_true', 'make_status_false']


    def make_status_true(self, request, queryset):
        updated = queryset.update(status=True)
        self.message_user(request, ngettext(
            '%d دسته بندی فعال شد.',
            '%d دسته بندی فعال شدند.',
            updated,
        ) % updated, messages.SUCCESS)
    make_status_true.short_description = "فعال کردن دسته بندی های انتخاب شده"

    def make_status_false(self, request, queryset):
        updated = queryset.update(status=False)
        self.message_user(request, ngettext(
            '%d دسته بندی غیرفعال شد.',
            '%d دسته بندی غیرفعال شدند.',
            updated,
        ) % updated, messages.SUCCESS)
    make_status_false.short_description = "غیرفعال کردن دسته بندی های انتخاب شده"


admin.site.register(Category, CategoryAdmin)

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'thumbnail_tag', 'slug', 'jpublish', 'status', 'category_to_str')
    list_filter = ('publish', 'status')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}
    ordering = ['status', 'publish']
    actions = ['make_published', 'make_drafted']

    def category_to_str(self, obj):
        return "، ".join([category.title for category in obj.category.active()])
    
    category_to_str.short_description = "دسته بندی"
    # Actions:
    def make_published(self, request, queryset):
        updated = queryset.update(status='p')
        self.message_user(request, ngettext(
            '%d مقاله با موفقیت منتشر شد.',
            '%d مقاله با موفقیت منتشر شدند.',
            updated,
        ) % updated, messages.SUCCESS)

    make_published.short_description = "انتشار مقالات انتخاب شده"

    def make_drafted(self, request, queryset):
        updated = queryset.update(status='d')
        self.message_user(request, ngettext(
            '%d مقاله با موفقیت پیش نویس شد.',
            '%d مقاله با موفقیت پیش نویس شدند.',
            updated,
        ) % updated, messages.SUCCESS)

    make_drafted.short_description = "پیشنویس کردن مقالات انتخاب شده"


admin.site.register(Article, ArticleAdmin)