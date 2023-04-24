from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Category, Books, Author, Publisher, AvailableBook, Borrower, Borrow, 
from datetime import datetime, timedelta
from django.shortcuts import render, redirect
from django.contrib.auth.models import User


class MyLoginView(LoginView):
    redirect_authenticated_user = True
    template_name = 'login.html'

    def get_success_url(self):
        return reverse_lazy('home')


class MyLogoutView(LogoutView):
    redirect_field_name = True

# Book views
class BookListView(ListView):
    model = Books
    template_name = 'book_list.html'

class BookCreateView(CreateView):
    model = Books
    fields = ['title', 'author', 'publisher', 'public_date', 'cover', 'description', 'category']
    template_name = 'book_form.html'

class BookUpdateView(UpdateView):
    model = Books
    fields = ['title', 'author', 'publisher', 'public_date', 'cover', 'description', 'category']
    template_name = 'book_form.html'

class BookDeleteView(DeleteView):
    model = Books
    success_url = reverse_lazy('book_list')
    template_name = 'book_confirm_delete.html'


# Borrower views
class BorrowerCreateView(CreateView):
    model = Borrower
    fields = ['user']
    template_name = 'borrower_form.html'

class BorrowerUpdateView(UpdateView):
    model = Borrower
    fields = ['user', 'debt']
    template_name = 'borrower_form.html'

class BorrowerDeleteView(DeleteView):
    model = Borrower
    success_url = reverse_lazy('borrower_list')
    template_name = 'borrower_confirm_delete.html'


# Staff views
class StaffCreateView(CreateView):
    model = User
    fields = ['username', 'email', 'password']
    template_name = 'staff_form.html'

class StaffUpdateView(UpdateView):
    model = User
    fields = ['username', 'email', 'password']
    template_name = 'staff_form.html'

class StaffDeleteView(DeleteView):
    model = User
    success_url = reverse_lazy('staff_list')
    template_name = 'staff_confirm_delete.html'


# AvailableBook views
class AvailableBookListView(ListView):
    model = AvailableBook
    template_name = 'available_book_list.html'

class AvailableBookCreateView(CreateView):
    model = AvailableBook
    fields = ['book', 'status']
    template_name = 'available_book_form.html'

class AvailableBookUpdateView(UpdateView):
    model = AvailableBook
    fields = ['book', 'status']
    template_name = 'available_book_form.html'

class AvailableBookDeleteView(DeleteView):
    model = AvailableBook
    success_url = reverse_lazy('available_book_list')
    template_name = 'available_book_confirm_delete.html'


# Borrow views
class BorrowListView(LoginRequiredMixin, ListView):
    model = Borrow
    template_name = 'borrow_list.html'

class BorrowCreateView(CreateView):
    model = Borrow
    fields = ['borrower', 'borrowed_book', 'status', 'issued_date', 'expiry_date']
    template_name = 'borrow_form.html'

class BorrowUpdateView(UpdateView):
    model = Borrow
    fields = ['borrower', 'borrowed_book', 'status', 'issued_date', 'expiry_date']
    template_name = 'borrow_form.html'

class BorrowDeleteView(DeleteView):
    model = Borrow
    success_url = reverse_lazy('borrow_list')
    template_name = 'borrow_confirm_delete.html'

