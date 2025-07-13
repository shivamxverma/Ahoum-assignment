import React, { useState, useEffect } from "react";
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Dashboard from './pages/dashboard.jsx';
import { AuthProvider } from './config/Auth.config.jsx';
import ProtectedRoute from './config/ProtectedRoute.jsx';
import Login from './pages/login.jsx';
import SignupForm from './pages/signup.jsx';
import FacilitatorDashboard from './pages/facilitator-dashboard.jsx';

function App() {
  const [role, setRole] = useState(null);

  useEffect(() => {
    const storedRole = localStorage.getItem('role');
    setRole(storedRole || null); 
  }, []);

  console.log('User Role:', role);

  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/signup" element={<SignupForm />} />
          <Route
            path="/"
            element={
              <ProtectedRoute>
                {role === 'User' ? <Dashboard /> : <FacilitatorDashboard />}
              </ProtectedRoute>
            }
          />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}

export default App;