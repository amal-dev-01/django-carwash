
from django.urls import path,include
from .import views

urlpatterns = [
    path('',views.sign_up,name='signup'),
    path('login/',views.loginUser,name='login'),
    path('logout/',views.logoutUser,name='logout'),
    # path('home/',views.home,name='home'),
    path('otp/<str:name>/<int:id>/',views.otpView,name='otp'),
    path('forgotpassword/',views.forgotPassword,name='forgotpass'),
    path('restpassword/<int:id>/',views.restPassword,name='restpass'),
    path('loginwithotp/',views.loginwithotp,name='loginwithotp'),
    
]