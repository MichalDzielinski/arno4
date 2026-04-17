from django.db import models
from django.urls import reverse
from django_extensions.db.fields import AutoSlugField

class Category(models.Model):
    name= models.CharField(max_length=250, db_index=True)
    slug = AutoSlugField(populate_from='name')

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('category list', args=[self.slug])

class Product(models.Model):
    category = models.ForeignKey(Category, related_name='product', on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=250)
    brand = models.CharField(max_length=250, default = 'un-branded')
    description = models.TextField(blank=True)
    slug = AutoSlugField(populate_from='title')
    price = models.DecimalField(max_digits=4, decimal_places=2)
    image = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('product info', args=[self.slug])







