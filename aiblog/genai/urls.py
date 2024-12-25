from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup_view, name='signup'),
    path('', views.genai, name='genai'),  # URL for URL processing
 path('blogs/', views.blog_list, name='blog_list'),
    path('blog/<int:id>/', views.blog_detail, name='blog_detail'),

]
