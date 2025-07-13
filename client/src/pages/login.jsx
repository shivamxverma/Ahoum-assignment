import React from 'react';
import { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
// import jwtDecode from 'jwt-decode'; 

const Login = () => {
  const navigate = useNavigate(); // Changed variable name to convention
  const [success, setSuccess] = useState(false);
  const [error, setError] = useState(null);
  const [role, setRole] = useState('User');
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const handleLogin = async () => {
    try {
      const response = await axios.post('http://127.0.0.1:5000/api/login', {
        username,
        password,
        role // Added role to the request body
      });

      console.log('Login successful:', response.data);
      const userId = response.data.userId;
      localStorage.setItem('token', response.data.token);
      localStorage.setItem('userId', userId);

      // Decode token to get user info
      // const user = jwtDecode(response.data.token);
      // console.log('User Info:', user);
      
      setSuccess(true);
      setError(null);
      localStorage.setItem('role', role);
      
      // Store user info in localStorage
      // localStorage.setItem('user', JSON.stringify(user));
      
      // Reset form fields
      setUsername('');
      setPassword('');
      
      // Delay navigation slightly to show success message
      setTimeout(() => {
        navigate('/'); // Changed to use navigate instead of navigator
      }, 1000);
    } catch (error) {
      const errorMessage = error.response?.data?.message || 'Login failed. Please try again.';
      console.error('Login failed:', errorMessage);
      setError(errorMessage);
      setSuccess(false);
    }
  };

  // Handle form submission on Enter key
  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      handleLogin();
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100">
      <div className="bg-white p-8 rounded-lg shadow-lg w-full max-w-md">
        {success && (
          <div className="bg-green-100 text-green-800 p-4 rounded-md mb-4">
            Login successful! Redirecting to dashboard...
          </div>
        )}
        {error && (
          <div className="bg-red-100 text-red-800 p-4 rounded-md mb-4">
            {error}
          </div>
        )}
        
        <h2 className="text-2xl font-bold mb-6 text-center text-gray-800">Login</h2>
        <div className="space-y-4">
          <div>
            <label htmlFor="role" className="block text-sm font-medium text-gray-700">Role</label>
            <select
              id="role"
              value={role}
              onChange={(e) => setRole(e.target.value)}
              className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 text-black"
            >
              <option value="User">User</option>
              <option value="Facilitator">Facilitator</option>
            </select>
          </div>
          <div>
            <label htmlFor="username" className="block text-sm font-medium text-gray-700">Username or Email</label>
            <input
              type="text"
              id="username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              onKeyPress={handleKeyPress}
              className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 text-black"
              placeholder="Enter your username or email"
              required
            />
          </div>
          <div>
            <label htmlFor="password" className="block text-sm font-medium text-gray-700">Password</label>
            <input
              type="password"
              id="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              onKeyPress={handleKeyPress}
              className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 text-black"
              placeholder="Enter your password"
              required
            />
          </div>
          <button
            onClick={handleLogin}
            disabled={!username || !password} // Disable button if fields are empty
            className="w-full bg-indigo-600 text-white py-2 px-4 rounded-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 disabled:bg-indigo-300 disabled:cursor-not-allowed"
          >
            Login
          </button>
        </div>
        <p className="mt-4 text-center text-sm text-gray-600">
          Don't have an account?{' '}
          <a href="/signup" className="text-indigo-600 hover:underline">Sign up</a>
        </p>
      </div>
    </div>
  );
};

export default Login;