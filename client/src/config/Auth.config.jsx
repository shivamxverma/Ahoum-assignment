import React, { createContext, useState, useEffect } from 'react';

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [role, setRole] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const storedRole = localStorage.getItem('role');
    const token = localStorage.getItem('token'); // Assuming you store a token
    setRole(storedRole || null);
    setIsLoading(false); // Set loading to false after retrieving data
  }, []);

  return (
    <AuthContext.Provider value={{ role, setRole, isLoading }}>
      {children}
    </AuthContext.Provider>
  );
};