import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Dashboard from './pages/dashboard.jsx';
import { AuthProvider, AuthContext } from './config/Auth.config.jsx';
import ProtectedRoute from './config/ProtectedRoute.jsx';
import Login from './pages/login.jsx';
import SignupForm from './pages/signup.jsx';
import FacilitatorDashboard from './pages/facilitator-dashboard.jsx';

function App() {
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
                <AuthContext.Consumer>
                  {({ role, isLoading }) =>
                    isLoading ? (
                      <div>Loading...</div>
                    ) : (
                      <>
                        {role === 'User' ? (
                          <Dashboard />
                        ) : role === 'Facilitator' ? (
                          <FacilitatorDashboard />
                        ) : (
                          <div>Loading...</div>
                        )}
                      </>
                    )
                  }
                </AuthContext.Consumer>
              </ProtectedRoute>
            }
          />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}

export default App;