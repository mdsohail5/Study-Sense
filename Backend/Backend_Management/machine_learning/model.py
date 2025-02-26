import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from Backend_Management.models import StudyData, ExamMarks

class StudyPrediction:
    def __init__(self, user):
        self.user = user

    def fetch_data(self):
        """Fetch StudyData and ExamMarks for the user."""
        study_data = StudyData.objects.filter(user=self.user)
        exam_data = ExamMarks.objects.filter(user=self.user)
        return study_data, exam_data

    def train_model(self, study_data, exam_data):
        """Train model using study data and exam marks data."""
        X = []
        y = []

        # Map study data to features (study hours and difficulty level)
        for study in study_data:
            for exam in exam_data.filter(subject=study.study_topic):
                X.append([study.study_hours, study.difficulty_level == 'Hard', study.difficulty_level == 'Medium'])
                y.append(exam.marks_obtained)

        X = np.array(X)
        y = np.array(y)

        # Simple linear regression model
        if len(X) == 0:  # If no data, return a default prediction (could be improved)
            return 0

        # Simple regression using numpy
        coef, intercept = np.linalg.lstsq(X, y, rcond=None)[0]
        return coef, intercept

    def predict_marks(self, study_hours, difficulty_level, coef, intercept):
        """Predict the marks based on study hours and difficulty level."""
        difficulty_features = [difficulty_level == 'Hard', difficulty_level == 'Medium']
        prediction = np.dot([study_hours] + difficulty_features, coef) + intercept
        return prediction

    def suggest_study_hours(self, desired_score, coef, intercept, difficulty_level):
        """Suggest the study hours needed to achieve the desired score."""
        difficulty_features = [difficulty_level == 'Hard', difficulty_level == 'Medium']
        suggested_study_hours = (desired_score - intercept) / coef[0]
        return suggested_study_hours
