import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split
from .models import StudyData, ExamMarks
from django.db import models

def train_model_from_db(user, subject):
    try:
        # Try reading the CSV files for study data and exam marks
        study_data = pd.read_csv("study_data.csv")
        exam_marks = pd.read_csv("exam_marks.csv")
    except FileNotFoundError:
        # If the files are not found, create default entries
        study_data = [
            {"user_id": 1, "study_hours": 5.0, "study_topic": "Math", "study_date": "2023-09-01"},
            {"user_id": 1, "study_hours": 3.5, "study_topic": "Math", "study_date": "2023-09-05"},
            {"user_id": 1, "study_hours": 6.0, "study_topic": "Science", "study_date": "2023-09-02"},
            {"user_id": 1, "study_hours": 4.5, "study_topic": "Science", "study_date": "2023-09-10"},
            {"user_id": 2, "study_hours": 2.5, "study_topic": "English", "study_date": "2023-09-03"},
        ]
        # Define the default exam marks entries
        exam_data = [
            {"user_id": 1, "subject": "Math", "exam_date": "2023-09-10", "hours_studied": 8.5, "marks_obtained": 78},
            {"user_id": 1, "subject": "Science", "exam_date": "2023-09-15", "hours_studied": 10.0, "marks_obtained": 85},
            {"user_id": 2, "subject": "English", "exam_date": "2023-09-12", "hours_studied": 6.5, "marks_obtained": 72},
        ]
    
    # Convert study data and exam data to pandas DataFrame
    study_df = pd.DataFrame(study_data)
    exam_df = pd.DataFrame(exam_data)

    # Merge the two dataframes based on user_id and subject
    study_df["study_date"] = pd.to_datetime(study_df["study_date"])
    exam_df["exam_date"] = pd.to_datetime(exam_df["exam_date"])

    # Merge data by user and subject
    merged_data = pd.merge(exam_df, study_df, left_on=["user_id", "subject"], right_on=["user_id", "study_topic"])

    # Group by user and subject and aggregate study hours and marks
    merged_data = merged_data.groupby(["user_id", "subject"]).agg({"study_hours": "sum", "marks_obtained": "mean"}).reset_index()

    # Prepare features (X) and labels (y)
    X = merged_data[["study_hours"]]
    y = merged_data["marks_obtained"]

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train a Linear Regression model
    model = LinearRegression()
    model.fit(X_train, y_train)
    
    # Predict on the test set
    y_pred = model.predict(X_test)
    
    # Calculate the Mean Absolute Error (MAE)
    error = mean_absolute_error(y_test, y_pred)
    print(f"Model Mean Absolute Error: {error:.2f}")
    
    return model, error


def predict_marks_ml(model, study_hours):
    """Predict marks based on the study hours using the trained model."""
    predicted_marks = model.predict([[study_hours]])[0]
    return min(100, max(0, round(predicted_marks, 2)))  # Ensure marks are between 0 and 100


def required_study_hours_ml(model, desired_marks):
    """Calculate the required study hours to achieve the desired marks using the trained model."""
    required_hours = (desired_marks - model.intercept_) / model.coef_[0]
    return max(0, round(required_hours, 2))  # Ensure study hours cannot be negative
