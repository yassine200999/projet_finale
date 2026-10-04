from django.db import models
class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    subcategory = models.ManyToManyField('SubCategory', related_name='products')
    def __str__(self):
        return self.name
class Image(models.Model):
    image_url = models.CharField(max_length=200)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    class Meta:
        db_table = 'image'
    # def __str__(self):
    #     return f"Image for {self.product.name}"