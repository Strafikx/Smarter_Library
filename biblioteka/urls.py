from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path(
        route='',
        view=login_required(views.BookListView.as_view()),
        name='home'
    )
]