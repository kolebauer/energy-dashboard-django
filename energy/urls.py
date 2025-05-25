from django.urls import path
from . import views

# Maps URL paths to their corresponding view functions
urlpatterns = [
    path('', views.home, name='home'),                     # Homepage
    path('upload/', views.upload_csv, name='upload'),      # CSV upload and stats page
    path('visualize/', views.visualize, name='visualize')  # Line chart page
]
