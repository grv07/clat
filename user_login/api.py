# from student.models import Student
# from .serializer import StudentSerializer
# from rest_framework import generics, permissions
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework.decorators import api_view


# class StudentViewSet(generics.ListCreateAPIView):
#     """
#     API endpoint that allows users to be viewed or edited.
#     """
#     queryset = Student.objects.all()
#     serializer_class = StudentSerializer


# class StudentObject(APIView):
#     permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

#     def get(self, request, pk, format=None):
#         student = Student.objects.get(pk=pk)
#         stu_serializer = StudentSerializer(student)
#         return Response(stu_serializer.data)


# class CreateStudent(APIView):
#     permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    
#     def post(self, request, format=None):
#         print request.DATA
