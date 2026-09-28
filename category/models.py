from django.db import models
class Category(models.Model):
    name=models.CharField(max_length=100,unique=True)
    description = models.TextField(blank=True)
    def __str__(self):
        return self.name
class SubCategory(models.Model):
    name=models.CharField(max_length=100,unique=True)
    category=models.ForeignKey(Category,on_delete=models.CASCADE,related_name="SubCategory")
    def __str__(self):
        return f"{self.name}({self.category.name})"