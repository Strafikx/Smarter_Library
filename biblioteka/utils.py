
from django.shortcuts import redirect

from .models import Borrower, Borrow

from django.utils import timezone as tz


def clear_fine(request, pk):
    borrower = Borrower.objects.get(id=pk)
    borrower.debt = 0
    borrower.save()

    return redirect('borrower-detail', pk=borrower.id)


def end_borrow(request, pk):
    borrower = Borrower.objects.get(id=pk)

    last_borrow = Borrow.objects.filter(borrower=borrower).latest('expiry_date')
    last_borrow.end = tz.now()
    last_borrow.status = 0
    last_borrow.save()

    return redirect('borrower-detail', pk=pk)