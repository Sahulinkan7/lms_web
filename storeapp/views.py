from django.shortcuts import render
from .models import Course,Level

def courses_view(request):
    courses=Course.objects.all()
    levels=Level.objects.all()
    freecourse_count=Course.objects.filter(price=0).count()
    paidcourse_count=Course.objects.filter(price__gte=1).count()
    context={
        'courses':courses,
        'levels':levels,
        'freecoursecount':freecourse_count,
        'paidcoursecount':paidcourse_count}
    return render(request,"storeapp/courses.html",context)

def search_course(request):
    query=request.GET['query']
    searchedcourses=Course.objects.filter(title__icontains=query)
    return render(request,"storeapp/search.html",{'searchedcourses':searchedcourses})

def course_details(request,slug):
    return render(request,"storeapp/course_details.html")
