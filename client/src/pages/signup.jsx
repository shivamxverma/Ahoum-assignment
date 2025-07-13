import React, { useState } from 'react';
import { GoogleOAuthProvider, GoogleLogin } from '@react-oauth/google';
import axios from 'axios';

function SignupForm() {
  const [role, setRole] = useState('user');
  const [formData, setFormData] = useState({
    name: '',
    username: '',
    email: '',
    password: '',
    confirmPassword: '',
    phone: ''
  });
  const [showPassword, setShowPassword] = useState(false);
  const [passwordMatch, setPasswordMatch] = useState(true);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => {
      const updatedData = { ...prev, [name]: value };
      if (name === 'password' || name === 'confirmPassword') {
        setPasswordMatch(updatedData.password === updatedData.confirmPassword);
      }
      return updatedData;
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (passwordMatch) {
      console.log('Form submitted:', { ...formData, role });
      // Replace console.log with your backend API call, e.g.:
      // axios.post('http://localhost:5000/api/signup', { ...formData, role });
    } else {
      alert('Passwords do not match!');
    }
  };

  const handleGoogleSuccess = async (credentialResponse) => {
    try {
      const response = await axios.post('http://localhost:5000/api/login/google', {
        access_token: credentialResponse.access_token,
        role
      });
      console.log('Google signup successful:', response.data);
    } catch (error) {
      console.error('Google signup failed:', error.response?.data || error.message);
    }
  };

  const handleGoogleError = () => {
    console.log('Google signup failed');
  };

  return (
    <GoogleOAuthProvider clientId="609437176807-pjbeho8loabcussbnvi0i09cqd81c45e.apps.googleusercontent.com">
      <div className="min-h-screen w-screen flex items-center justify-center bg-gray-100">
        <div className="bg-white p-8 rounded-lg shadow-lg w-full max-w-md">
          <h2 className="text-2xl font-bold mb-6 text-center text-black">Sign Up</h2>
          
          {/* Role Selection */}
          <div className="mb-6 flex justify-center space-x-4">
            <button
              className={`px-4 py-2 rounded-md font-medium ${role === 'user' ? 'bg-blue-500 text-black' : 'bg-gray-200 text-black'}`}
              onClick={() => setRole('user')}
            >
              User
            </button>
            <button
              className={`px-4 py-2 rounded-md font-medium ${role === 'facilitator' ? 'bg-blue-500 text-black' : 'bg-gray-200 text-black'}`}
              onClick={() => setRole('facilitator')}
            >
              Facilitator
            </button>
          </div>

          {/* Google Signup Button */}
          <div className="mb-4">
            <GoogleLogin
              onSuccess={handleGoogleSuccess}
              onError={handleGoogleError}
              text="signup_with"
              theme="outline"
              width="100%"
            />
          </div>

          <div className="text-center text-black mb-4">OR</div>

          {/* Form */}
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-black">Name</label>
              <input
                type="text"
                name="name"
                value={formData.name}
                onChange={handleInputChange}
                className="mt-1 w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 text-black"
                placeholder="Enter your name"
                required
              />
            </div>

            {role === 'user' && (
              <div>
                <label className="block text-sm font-medium text-black">Username</label>
                <input
                  type="text"
                  name="username"
                  value={formData.username}
                  onChange={handleInputChange}
                  className="mt-1 w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 text-black"
                  placeholder="Enter your username"
                  required
                />
              </div>
            )}

            <div>
              <label className="block text-sm font-medium text-black">Email</label>
              <input
                type="email"
                name="email"
                value={formData.email}
                onChange={handleInputChange}
                className="mt-1 w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 text-black"
                placeholder="Enter your email"
                required
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-black">Password</label>
              <input
                type={showPassword ? 'text' : 'password'}
                name="password"
                value={formData.password}
                onChange={handleInputChange}
                className="mt-1 w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 text-black"
                placeholder="Enter your password"
                required
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-black">Confirm Password</label>
              <input
                type={showPassword ? 'text' : 'password'}
                name="confirmPassword"
                value={formData.confirmPassword}
                onChange={handleInputChange}
                className={`mt-1 w-full px-3 py-2 border ${passwordMatch ? 'border-gray-300' : 'border-red-500'} rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 text-black`}
                placeholder="Confirm your password"
                required
              />
              {!passwordMatch && (
                <p className="text-red-500 text-sm mt-1">Passwords do not match</p>
              )}
            </div>

            <div className="flex items-center">
              <input
                type="checkbox"
                id="showPassword"
                checked={showPassword}
                onChange={() => setShowPassword(prev => !prev)}
                className="mr-2"
              />
              <label htmlFor="showPassword" className="text-sm text-black">Show Password</label>
            </div>

            {role === 'facilitator' && (
              <div>
                <label className="block text-sm font-medium text-black">Phone</label>
                <input
                  type="tel"
                  name="phone"
                  value={formData.phone}
                  onChange={handleInputChange}
                  className="mt-1 w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 text-black"
                  placeholder="Enter your phone number"
                  required
                />
              </div>
            )}

            <button
              type="submit"
              className="w-full bg-blue-500 text-black py-2 rounded-md hover:bg-blue-600 transition duration-200 disabled:bg-gray-400 disabled:text-black"
              disabled={!passwordMatch}
            >
              Sign Up
            </button>
          </form>
        </div>
      </div>
    </GoogleOAuthProvider>
  );
}

export default SignupForm;