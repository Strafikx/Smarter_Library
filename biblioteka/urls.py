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
        view=login_required(views.BookDeleteView.as_view()),
        name='book-delete'
    ),
    # path(
    #     route='create-user',
    #     view=login_required(views.CreateUserView.as_view()),
    #     name='create-user'
    # ),
    # path(
    #     route='user-list',
    #     view=login_required(views.UserListView.as_view()),
    #     name='user-list'
    # ),
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
        route='borrow/<str:exemplar>',
        view=login_required(views.BorrowCreateView.as_view()),
        name='borrow'
    )

]