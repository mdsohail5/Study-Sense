import React from 'react';
import { Navigate } from 'react-router-dom';

const ProtectedRoute = ({ children }) => {
  const token = localStorage.getItem('token');
  console.log('Token in ProtectedRoute:', token);  // For debugging

  return token ? children : <Navigate to="/login" />;
};

export default ProtectedRoute;
