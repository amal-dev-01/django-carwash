from django.urls import path
from . import views

urlpatterns = [
    path('payment/<int:id>/',views.payment,name='payment'),
    path('success/',views.success,name='success'),
    path('pdf/<int:id>/',views.pdf,name='pdf')

]
