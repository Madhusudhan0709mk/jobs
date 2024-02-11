# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
     path('register/',views.register,name="register"),
    path('login/',views.login,name="login"),
    path('logout/',views.logout,name='logout'),
    path('profile/view/', views.profile_view, name='profile_view'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
    path('listprofiles/',views.listprofiles,name='listprofiles'),
    path('create_job_posts/',views.create_job_posts,name='create_job_posts'),
    path('viewjobdetails/<int:pk>/',views.viewjobdetails,name='viewjobdetails'),

]
