from django.urls import path 
from . import views 

urlpatterns = [
    path("registration/",views.registration_view,name="registration"),
    path('login/',views.login_view,name="login"),
    path('logout/',views.logout_view,name="logout"),
    path("verify/<authtoken>/",views.verify_usermail,name="verify"),
    path("forgot_password/",views.forgot_password,name="forgot_password"),
    path("reset_password/<token>/",views.verify_password_reset_link,name="verify_password_reset_url"),
    path("account_profile/",views.update_profile,name="account_profile"),
]
