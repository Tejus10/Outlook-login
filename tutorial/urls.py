from django.urls import path

from . import views

urlpatterns = [
  # /tutorial
  path('', views.home, name='home'),
  path('signin/', views.sign_in, name='signin'),
  path('callback/', views.callback, name='callback'),
  path('signout/', views.sign_out, name='signout'),
  path('search/', views.search_ques, name='search_ques'),
  path('myquestions/', views.my_ques, name='my_ques'),
  path('all/', views.all, name='all'),  
]