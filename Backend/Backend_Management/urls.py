from django.urls import path
from .views import (
    UserRegisterView,
    UserLoginView,
    HomePageView,
    ToDoTaskCreateView,
    ToDoTaskDetailView,
    ExamMarksListCreateView,
    StudyDataListCreateView,
    StudyDataDetailView,
    ExamMarksDetailView,
    StudyDataListCreateView,
    StudyDataDetailView,
    ExamMarksListCreateView,
    ExamMarksDetailView,
    PredictMarksView,
    PredictMarksView, 
    RequiredStudyHoursView
)

urlpatterns = [
    # User Authentication Endpoints
    path('register/', UserRegisterView.as_view(), name='user-register'),
    path('login/', UserLoginView.as_view(), name='user-login'),
    
    # Home Page Endpoint
    path('home/', HomePageView.as_view(), name='home-page'),
    
    # Individual Endpoints for StudyData, ExamMarks, and other CRUD operations
    path('study-data/', StudyDataListCreateView.as_view(), name='study-data-list-create'),
    path('study-data/<int:pk>/', ToDoTaskDetailView.as_view(), name='study-data-detail'),
    
    path('exam-marks/', ExamMarksListCreateView.as_view(), name='exam-marks-list-create'),
    path('exam-marks/<int:pk>/', ExamMarksDetailView.as_view(), name='exam-marks-detail'),
    
    # CRUD Endpoints for tasks, goals, and alerts
    path('tasks/', ToDoTaskCreateView.as_view(), name='todo-list-create'),
    path('tasks/<int:pk>/', ToDoTaskCreateView.as_view(), name='todo-list-create'),
    path('predict-marks/', PredictMarksView.as_view(), name='predict-marks'),
    path('required-study-hours/', RequiredStudyHoursView.as_view(), name='required-study-hours'),
]
