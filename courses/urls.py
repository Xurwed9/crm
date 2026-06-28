from django.urls import path
from . import views

app_name = "courses"

urlpatterns = [
    path("", views.CourseListAPIView.as_view()),
    path("create/", views.CourseCreateAPIView.as_view()),
    path("<int:pk>/", views.CourseDetailAPIView.as_view()),
    path("<int:pk>/update/", views.CourseUpdateAPIView.as_view()),
    path("<int:pk>/delete/", views.CourseDeleteAPIView.as_view()),
]