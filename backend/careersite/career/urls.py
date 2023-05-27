from django.urls import path
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from django.shortcuts import redirect

from . import views
from django.urls import path, include

urlpatterns = [
    path('', lambda request: redirect('login'), name='login'),  # Redirect from root URL to login page
    path('home/', views.HomeView.as_view(),  name="home"),
    path('users/', views.UsersView.as_view(), name="users"),
    path('login/', views.LoginView.as_view(), name="login"),
    path('logout/', views.LogoutView.as_view(), name="logout"),
    path('signup/', views.SignUpView.as_view(), name="signup"),
    path('job-list/', views.JobListingsView.as_view(), name="job_list"),
    path('post-list/', views.PostListView.as_view(), name="post_list"),
    path('add-post/', views.AddPostView.as_view(), name="add_post"),
    path('delete-post/<int:post_id>', views.DeletePostView.as_view(), name="delete-post"),
    path('post-detail/<int:post_id>', views.PostDetailView.as_view(), name="post-detail"),
    path('delete-comment/<int:post_id>/<int:comment_id>', views.DeleteCommentView.as_view(), name="delete_comment"),
    path('create-job/', views.JobCreationView.as_view(), name="create_job"),

]



