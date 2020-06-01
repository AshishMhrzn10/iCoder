from django.contrib import admin
from django.urls import path, include
from blog import views
urlpatterns = [
    #API to post comment
    path('postcomment/',views.postComment,name="postComment"),
    path('', views.blogHome, name='blogHome'),
    path('<str:slug>/', views.blogPost, name='blogPost'),
]
