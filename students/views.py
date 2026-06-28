from rest_framework.viewsets import ModelViewSet
from .models import Student
from .serializers import StudentSerializer
from .permissions import IsAdminOrTeacher


class StudentViewSet(ModelViewSet):

    serializer_class = StudentSerializer
    permission_classes = [IsAdminOrTeacher]


    def get_queryset(self):

        user = self.request.user


        if user.role == "admin":
            return Student.objects.all()


        if user.role == "teacher":
            return Student.objects.none()


        return Student.objects.filter(
            user=user
        )