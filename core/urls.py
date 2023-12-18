from django.urls import path
from core import views 

urlpatterns = [
    path("",views.home_view,name="home_view"),
    path("about_us/",views.about_us,name="about_us_view"),
    path("contact_us/",views.contact_us,name="contact_us_view")
]
