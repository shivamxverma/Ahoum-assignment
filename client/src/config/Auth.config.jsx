import React, { createContext, useState, useEffect } from 'react';

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [role, setRole] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const storedRole = localStorage.getItem('role');
    const token = localStorage.getItem('token');
    console.log('Stored role:', storedRole);
    console.log('Token:', token);
    setRole(storedRole || null);
    setIsLoading(false); 
  }, []);

  return (
    <AuthContext.Provider value={{ role, setRole, isLoading }}>
      {children}
    </AuthContext.Provider>
  );
};