from django.urls import path
from .views import (
    GradeListAPIView,
    GradeDetailAPIView,
    GradeCreateAPIView,
    GradeUpdateAPIView,
    GradeDeleteAPIView,
)

urlpatterns = [
    # GET  /grades/                 -> list all grade records
    path("grades/", GradeListAPIView.as_view(), name="grade-list"),

    # GET  /grades/<id>/            -> view a single grade record
    path("grades/<int:pk>/", GradeDetailAPIView.as_view(), name="grade-detail"),

    # POST /grades/create/          -> create a new grade record
    path("grades/create/", GradeCreateAPIView.as_view(), name="grade-create"),

    # PATCH /grades/<id>/update/    -> update an existing grade record
    path("grades/<int:pk>/update/", GradeUpdateAPIView.as_view(), name="grade-update"),

    # DELETE /grades/<id>/delete/   -> delete a grade record
    path("grades/<int:pk>/delete/", GradeDeleteAPIView.as_view(), name="grade-delete"),
]
