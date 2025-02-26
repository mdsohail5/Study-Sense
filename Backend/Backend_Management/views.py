from django.contrib.auth.models import User
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import UserRegistrationSerializer, ToDoListSerializer, StudyDataSerializer, ExamMarksSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework import status
from .models import ToDoTask,  StudyData, ExamMarks
from rest_framework.permissions import AllowAny
from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import StudyData, ExamMarks
from .serializers import StudyDataSerializer, ExamMarksSerializer
from django.db.models import Sum

# User Registration View
class UserRegisterView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer  # Use a dedicated serializer for user registration
    queryset = User.objects.all()
    permission_classes = [AllowAny]  # Allow access to everyone for registration

# User Login View
class UserLoginView(generics.GenericAPIView):
    permission_classes = [AllowAny] 
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        user = User.objects.filter(username=username).first()
        if user and user.check_password(password):
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        return Response({'detail': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
 
class ToDoTaskCreateView(generics.ListCreateAPIView):
    serializer_class = ToDoListSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ToDoTask.objects.filter(user = self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ToDoTaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ToDoListSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ToDoTask.objects.filter(user = self.request.user)
    

class StudyDataListCreateView(generics.ListCreateAPIView):
    serializer_class = StudyDataSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return StudyData.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class StudyDataDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = StudyDataSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return StudyData.objects.filter(user=self.request.user)


class ExamMarksListCreateView(generics.ListCreateAPIView):
    serializer_class = ExamMarksSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ExamMarks.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ExamMarksDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ExamMarksSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ExamMarks.objects.filter(user=self.request.user)

class HomePageView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user

        # Fetch data for the logged-in user
        tasks = ToDoTask.objects.filter(user=user)
        exam_marks = ExamMarks.objects.filter(user=user)

        # Serialize the data
        tasks_data = ToDoListSerializer(tasks, many=True).data
        exam_marks_data = ExamMarksSerializer(exam_marks, many=True).data

        # Combine the data
        response_data = {
            "tasks": tasks_data,
            "exam_marks": exam_marks_data,
        }

        return Response(response_data, status=status.HTTP_200_OK)



from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .MLModel import train_model_from_db, predict_marks_ml, required_study_hours_ml

class PredictMarksView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        subject = request.query_params.get("subject")
        
        if not subject:
            return Response({"error": "Subject is required"}, status=400)
        
        model, error = train_model_from_db(user, subject)

        if model is None:
            return Response({"error": error}, status=400)

        study_hours = float(request.query_params.get("study_hours", 0))
        predicted_marks = predict_marks_ml(model, study_hours)
        return Response({"predicted_marks": predicted_marks})


class RequiredStudyHoursView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        subject = request.query_params.get("subject")
        
        if not subject:
            return Response({"error": "Subject is required"}, status=400)
        
        model, error = train_model_from_db(user, subject)

        if model is None:
            return Response({"error": error}, status=400)

        desired_marks = float(request.query_params.get("desired_marks", 0))
        required_hours = required_study_hours_ml(model, desired_marks)
        return Response({"required_study_hours": required_hours})
