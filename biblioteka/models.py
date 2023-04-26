from django.db import models
from django.contrib.auth.models import User


from datetime import datetime, timedelta


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
    

class AvailableBook(models.Model):
    STATUS_CHOICES = (
        (0, 'False'),
        (1, 'True'),
    )

    book = models.ForeignKey(Books, on_delete=models.CASCADE)
    status = models.IntegerField(choices=STATUS_CHOICES, default=1)
    


class Borrower(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    debt = models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.user
    
    def is_available(self):
        book = self.borrow_set.filter(status=1)

        if book:
            return book.first().availablebook

        return False

    def can_borrow_book(self):
        can_borrow = not (self.debt or self.borrow_set.filter(status=1))
        return can_borrow


    

def expiry():
    return datetime.today() + timedelta(days=14)

class Borrow(models.Model):
    STATUS_CHOICES = (
        (0, 'False'),
        (1, 'True'),
    )

    borrower = models.ForeignKey(Borrower, on_delete=models.CASCADE)
    borrowed_book = models.ForeignKey(AvailableBook, on_delete=models.CASCADE)
    status = models.IntegerField(choices=STATUS_CHOICES, default=1)
    issued_date = models.DateField(auto_now=True)
    expiry_date = models.DateField(default=expiry)

    def __str__(self) -> str:
        return f'{self.borrower} - {self.borrowed_book}'
    
    def debt(self):
        debt = (datetime.today - self.expiry_date).days
        
        if self.status and debt > 0:
            self.borrower.debt = debt
            self.borrower.save()
        