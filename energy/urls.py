from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  
    # Home page with links to both upload types

    path('upload_simple/', views.upload_simple, name='upload_simple'),  
    # Upload CSV for basic summary stats + line/bar charts - redirects to visualize()

    path('upload_advanced/', views.upload_advanced, name='upload_advanced'),  
    # Upload CSV for advanced statistical analysis - redirects to analyze()

    path('visualize/', views.visualize, name='visualize'),  
    # Page that renders basic visualizations (line + bar) from CSV data

    path('analyze/', views.analyze, name='analyze'),  
    # Page that renders extended analysis (daily mean/std, hourly var) from CSV
]
