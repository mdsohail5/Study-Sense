from .model import StudyPrediction

def make_prediction(user, study_hours, difficulty_level):
    study_prediction = StudyPrediction(user)
    predicted_marks = study_prediction.predict_marks(study_hours, difficulty_level)
    return predicted_marks

def suggest_hours_for_score(user, desired_score, difficulty_level):
    study_prediction = StudyPrediction(user)
    suggested_hours = study_prediction.suggest_study_hours(desired_score, difficulty_level)
    return suggested_hours
