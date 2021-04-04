from django.db import models
from django.utils import timezone
from extensions.utils import jalali_converter

# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=200, verbose_name='عنوان دسته بندی')
    slug = models.SlugField(max_length=100, unique=True, verbose_name='آدرس دسته بندی')
    status = models.BooleanField(default=True, verbose_name='آیا نمایش داده شود؟')
    position = models.IntegerField()

    class Meta:
        verbose_name = "دسته بندی"
        verbose_name_plural = "دسته بندی ها"
        ordering = ['position']

    def __str__(self):
        return self.title

class Article(models.Model):
    STATUS_CHOICES = [
        ('d', 'پیش نویس'),
        ('p', 'منتشر شده'),
    ]
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=100, unique=True)
    category = models.ManyToManyField(Category, verbose_name='دسته بندی')
    description = models.TextField()
    thumbnail = models.ImageField(upload_to='images')
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)

    class Meta:
        ordering = ['-publish']

    def __str__(self):
        return self.title

    def jpublish(self):
        return jalali_converter(self.publish)

    jpublish.short_description = "زمان انتشار"
    
