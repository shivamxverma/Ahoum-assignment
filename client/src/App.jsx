import React from "react";
import {BrowserRouter,Routes,Route} from 'react-router-dom';
import Dashboard from './pages/dashboard.jsx';
import { AuthProvider } from './config/Auth.config.jsx';
import ProtectedRoute from './config/ProtectedRoute.jsx';
import Login from './pages/login.jsx';
import SignupForm from './pages/signup.jsx'; 
import FacilitatorDashboard from './pages/facilitator-dashboard.jsx'

function App() {

  return (
    <>
      <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/signup" element={<SignupForm />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/facilitator-dashboard" element={<FacilitatorDashboard />} />
          <Route
            path="/"
            element={
              <ProtectedRoute>
                <Dashboard />
              </ProtectedRoute>
            }
          /> 
        </Routes>
      </BrowserRouter>
      </AuthProvider>
    </>
  );
}

export default App;
