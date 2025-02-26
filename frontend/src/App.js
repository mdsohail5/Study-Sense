import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Login from './Login';
import HomePage from './HomePage';
import ProtectedRoute from './ProtectedRoute';
import Register from './Register';
import StudyData from './StudyData';
import ExamMarks from './ExamMarks';

const App = () => {
  return (
    <Router>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/Register" element={<Register />} />
        <Route
          path="/"
          element={
            <ProtectedRoute>
              <HomePage />
            </ProtectedRoute>
          }
        /> 
        <Route
          path="/StudyHours"
          element={
            <ProtectedRoute>
              <StudyData />
            </ProtectedRoute>
          }
        /> 
        <Route
          path="/ExamMarks"
          element={
            <ProtectedRoute>
              <ExamMarks />
            </ProtectedRoute>
          }
        /> 
      </Routes>
    </Router>
  );
};

export default App;
