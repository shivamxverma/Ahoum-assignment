import React, { useContext } from 'react';
import { Navigate } from 'react-router-dom';
import { AuthContext } from './Auth.config.jsx';

const ProtectedRoute = ({ children }) => {
  const { role, isLoading } = useContext(AuthContext);
  const token = localStorage.getItem('token'); // Check token directly

  if (isLoading) {
    return <div>Loading...</div>; // Show loading while fetching auth data
  }

  if (!token || !role) {
    return <Navigate to="/login" replace />;
  }

  return children;
};

export default ProtectedRoute;