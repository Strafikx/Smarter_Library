from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path(
        route='',
        view=login_required(views.BooksListView.as_view()),
        name='home'
    ),
    path(
        route='login',
        view=views.MyLoginView.as_view(),
        name='login'
    ),
    path(
        route='logout',
        view=views.MyLogoutView.as_view(),
        name='logout'
    ),
    path(
        route='book-detail/<str:pk>',
        view=login_required(views.BookDetailView.as_view()),
        name='book-detail'
    ),
    path(
        route='book-create',
        view=login_required(views.BookCreateView.as_view()),
        name='book-create'
    ),
    path(
        route='book-edit/<str:pk>',
        view=login_required(views.BookUpdateView.as_view()),
        name='book-edit'
    ),
    path(
        route='book-delete/<str:pk>',
        view=login_required(views.BookDeleteView.as_view()), #not working
        name='book-delete'
    ),
    path(
        route='borrower-list',
        view=login_required(views.BorrowerListView.as_view()), #not working
        name='borrower-list'
    ),
    path(
        route='borrower-detail/<str:pk>',
        view=login_required(views.BorrowerDetailView.as_view()), #not working
        name='borrower-detail'
    ),
    path(
        route='borrower-update/<str:pk>',
        view=login_required(views.BorrowerUpdateView.as_view()),
        name='borrower-update'
    ),
    path(
        route='book-available-list/<str:book>',
        view=login_required(views.AvailableBookListView.as_view()),
        name='book-available-list'
    ),
    path(
        route='book-available-create/<str:book>',
        view=login_required(views.AvailableBookCreateView.as_view()),
        name='book-available-create'
    ),
    path(
        route='available-detail/<str:pk>',
        view=login_required(views.AvailableBookDetailView.as_view()),
        name='available-detail'
    ),
    path(
        route='borrow/<str:availableB>',
        view=login_required(views.BorrowCreateView.as_view()),
        name='borrow-create'
    )

]