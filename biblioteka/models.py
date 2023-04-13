from django.db import models

# Create your models here.

class Category(models.Model):
    cat_title = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.cat_title


class Books(models.Model):
    title = models.CharField(max_length=50)
    author = models.ForeignKey('Author', on_delete=models.CASCADE)
    publisher = models.ForeignKey('Publisher', on_delete=models.CASCADE)
    public_date = models.DateField(auto_now_add=True)
    cover = models.ImageField(upload_to='covers',null=True, blank=True)
    description = models.TextField(blank=True, null=True,)
    category = models.ManyToManyField(Category)

    def __str__(self) -> str:
        return self.title


class Author(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()

    def __str__(self) -> str:
        return self.name


class Publisher(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=150)

    def __str__(self) -> str:
        return self.name
    

#check
