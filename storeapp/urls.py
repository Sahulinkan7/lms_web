from django.urls import path 
from . import views

urlpatterns = [
    path("all_courses/",views.courses_view,name="courses_view"),
    path("search/",views.search_course,name="search_course"),
    path("course_details/<slug:slug>/",views.course_details,name="course_details"),
]
