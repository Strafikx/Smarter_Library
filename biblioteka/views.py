from .models import Books, AvailableBook, Borrow, Borrower
from django.db.models import Count
from django.core.mail import send_mail
from django.utils import timezone
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy, reverse
from django.contrib.auth.models import User
from .Forms import MyUserCreationForm

from django.db.models import Count
from django.db.models import Q



# Login 

class MyLoginView(LoginView):
    redirect_authenticated_user = True
    template_name = 'login.html'

    def get_success_url(self):
        return reverse_lazy('home')

class MyLogoutView(LogoutView):
    redirect_field_name = True

# Login end


# Book's views 


class BooksListView(ListView):
    model = Books
    template_name = 'home.html'
    context_object_name = 'books'
    paginate_by = 1

    def get_queryset(self):
        search = self.request.GET.get('search', '')
        queryset = super().get_queryset().filter(
            Q(title__icontains=search) |
            Q(author__name__icontains=search)
        )

        return queryset


class BookDetailView(DetailView):
    model = Books
    template_name = 'book-detail.html'

    # def get_context_data(self, **kwargs):
    #     context = super(BookDetailView, self).get_context_data(**kwargs)
    #     context['instances'] = len(AvailableBook.objects.filter(book=context['book'].id))

    #     return context


class BookCreateView(CreateView):
    model = Books
    template_name = 'form.html'
    fields = '__all__'
    success_url = reverse_lazy('home')


class BookUpdateView(UpdateView):
    model = Books
    template_name = 'form.html'
    fields = '__all__'

    def get_success_url(self):
        pk = self.kwargs["pk"]
        return reverse('book-detail', kwargs={"pk": pk})


class BookDeleteView(DeleteView):
    model = Books
    template_name = 'delete.html'
    success_url = reverse_lazy('home')

# Book's views end

# Borrow views

class BorrowCreateView(CreateView):
    model = Borrow
    fields = ['borrower']
    success_url = reverse_lazy('home')
    template_name = 'form.html'

    def form_valid(self, form):
        LastBorrow = Borrow.objects.filter(borrower=form.instance.borrower).last()

        if form.instance.borrower.debt:
            form.add_error('borrower', 'Fine isn\'t paid')

            return self.form_invalid(form)

        if LastBorrow is not None and timezone.now() < LastBorrow.end:
            form.add_error('borrower', 'You allready borrowed a book')

            return self.form_invalid(form)

        availableB = AvailableBook.objects.get(id=self.kwargs['avalaibleB'])
        availableB.status = 0
        availableB.save()

        form.instance.availableB = availableB

        response = super().form_valid(form)
        return response

    def get_success_url(self):
        return reverse_lazy('AvailableBook_detail', kwargs={'pk': self.object.availableB.id})
    
    # Borrow views end

    # Borrower views

class BorrowerListView(ListView):
    model = Borrower
    template_name = 'borrower_list.html'
    context_object_name = 'users'
    ordering = 'id'

    def get_queryset(self):
        search = self.request.GET.get('search', '')
        print(search)


        queryset = super().get_queryset().filter(
            Q(user__first_name__icontains=search)
        )

        for borrow in Borrow.objects.filter(status=1):
            borrow.calculate_fine()

        return queryset


class BorrowerDetailView(DetailView):
    model = Borrower
    template_name = 'borrower_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['availableB'] = self.object.has_availableB()

        return context


class BorrowerCreateView(CreateView):
    model = User
    form_class = MyUserCreationForm
    template_name = 'form.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        password = User.objects.make_random_password()

        user = form.save(commit=False)
        user.set_password(password)
        user.save()

        borrower = Borrower(user=user)
        borrower.save()

        send_mail(
            'Account has been created',
            f'Your passwords for {user.username} account: {password}',
            'ДОБАВИТЬ ИМЕЙЛ',
            [user.email],
        )

        response = super().form_valid(form)
        return response


class BorrowerUpdateView(UpdateView):
    model = Borrower
    form_class = MyUserCreationForm
    template_name = 'form.html'

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy('borrower_detail', kwargs={'pk': self.object.borrower.id})
    
# Borrower views end

# AvailableBooks views 

class AvailableBookListView(ListView):
    template_name = 'AvailableBook_list.html'
    context_object_name = 'AvailableBooks'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        context['book'] = self.kwargs['book']
        return context

    def get_queryset(self):
        AvailableBooks = AvailableBook.objects.filter(book=self.kwargs['book'])

        for availableB in AvailableBooks:

            borrows = Borrow.objects.filter(availableB=availableB)

            if not (borrows and borrows.latest('end').status):
                availableB.status = 1
                availableB.save()

            else:
                availableB.status = 0
                availableB.save()

                borrows.latest('end').availableB = availableB
                borrows.latest('end').save()

        return AvailableBooks


class AvailableBookDetailView(DetailView):
    model = AvailableBook
    template_name = 'AvailableBook_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        borrow = Borrow.objects.filter(exemplar=kwargs.get('object'))

        if borrow and borrow.latest('end').status:
            borrower = borrow.latest('end').borrower
        else:
            borrower = 'none'

        context['borrower'] = borrower

        return context


class AvailableBookCreateView(CreateView):
    model = AvailableBook
    fields = ['publisher', 'code']
    success_url = reverse_lazy('home')
    template_name = 'form.html'

    def form_valid(self, form):
        form.instance.book = Books.objects.get(id=self.kwargs['book'])
        response = super().form_valid(form)
        return response

    def get_success_url(self, **kwargs):
        return reverse_lazy('AvailableBooks_list', kwargs={"book": self.object.book.id})

# AvailableBook views end