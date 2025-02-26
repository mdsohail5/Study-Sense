from django.contrib.auth.models import User
from rest_framework import serializers
from .models import ToDoTask, StudyData, ExamMarks

class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class ToDoListSerializer(serializers.ModelSerializer):
        class Meta:
            model = ToDoTask
            fields = ['id', 'title', 'description', 'completed']
            read_only_fields = ['user', 'created_at']


class StudyDataSerializer(serializers.ModelSerializer):
     class Meta:
        model = StudyData  # Specify the model
        fields = '__all__' 
        read_only_fields = ['user', 'created_at']


class ExamMarksSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamMarks
        fields = '__all__'
        read_only_fields = ['user', 'created_at']
