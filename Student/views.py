from django.shortcuts import render,redirect
from .models import *
from django.http import HttpResponse
#from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q,Sum

from django.contrib.auth import get_user_model
User= get_user_model()


def get_students(request):
    queryset= Student.objects.all() 


    if request.GET.get('search'):
        Search= request.GET.get('search')
        queryset= queryset.filter(
            Q(student_name__icontains=Search) |
            Q(department__department__icontains=Search) 
        )

    paginator = Paginator(queryset, 10)  # Show 25 contacts per page.
    page_number = request.GET.get("page",1)
    page_obj = paginator.get_page(page_number)

    return render(request, 'report/students.html', {'queryset':page_obj})


from .seed import generate_report_card
def see_marks(request, student_id):
    queryset= SubjectMarks.objects.filter(student__student_id__student_id= student_id)
    total_marks= queryset.aggregate(total_marks= Sum('marks'))

    return render(request, 'report/see_marks.html', {'queryset':queryset, 'total_marks': total_marks})
