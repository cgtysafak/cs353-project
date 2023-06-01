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
    path('job-list/', views.JobListingsView.as_view(), name="job-list"),
    path('application-list/', views.PastApplicationsView.as_view(), name="application-list"),
    path('past-openings/', views.PastOpeningsView.as_view(), name="past-openings"),
    path('job-detail/<int:job_id>', views.JobDescriptionView.as_view(), name="job-detail"),
    path('post-list/', views.PostListView.as_view(), name="post-list"),
    path('add-post/', views.AddPostView.as_view(), name="add-post"),
    path('delete-post/<int:post_id>', views.DeletePostView.as_view(), name="delete-post"),
    path('post-detail/<int:post_id>', views.PostDetailView.as_view(), name="post-detail"),
    path('delete-comment/<int:comment_id>', views.DeleteCommentView.as_view(), name="delete-comment"),
    path('add-job/', views.AddJobView.as_view(), name="add-job"),

]



