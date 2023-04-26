from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Books)
admin.site.register(AvailableBook)
admin.site.register(Borrower)
admin.site.register(Borrow)
admin.site.register(Author)
admin.site.register(Publisher)
admin.site.register(Category)