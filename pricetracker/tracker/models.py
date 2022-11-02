from django.db import models

# Create your models here.
class Product(models.Model):
    title = models.CharField(max_length=256)
    url = models.URLField(max_length=512)
    slug = models.SlugField()
    list_price = models.DecimalField(max_digits=10, decimal_places=2)
    sell_price = models.DecimalField(max_digits=10, decimal_places=2)
    date_added = models.DateField(auto_now_add=True)