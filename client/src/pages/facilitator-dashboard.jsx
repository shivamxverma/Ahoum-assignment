import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

const FacilitatorDashboard = () => {
  const navigate = useNavigate();
  const [sessions, setSessions] = useState([]);
  const [editingSession, setEditingSession] = useState(null);
  const [formData, setFormData] = useState({ client: '', date: '', time: '', status: '' });
  const [showUsers, setShowUsers] = useState(null);
  const [error, setError] = useState(null);

  const fetchSessions = async () => {
    try {
      const response = await axios.get('http://127.0.0.1:5000/api/sessions');
      console.log('Fetched sessions:', response.data);
      const transformedSessions = response.data.map(session => ({
        id: session.id,
        client: session.name, // Backend's 'name' is mapped to 'client' for frontend
        date: session.start_time.split('T')[0], // Extract date (YYYY-MM-DD)
        time: new Date(session.start_time).toLocaleTimeString('en-US', {
          hour: '2-digit',
          minute: '2-digit',
          hour12: true,
        }), // Convert to 12-hour format (e.g., 10:00 AM)
        status: session.bookings.length > 0 ? session.bookings[0].status : 'Pending',
        registeredUsers: session.bookings.map(booking => booking.user_id),
        facilitator: session.facilitator ? session.facilitator.name : 'Unassigned',
      }));
      setSessions(transformedSessions);
    } catch (error) {
      console.error('Error fetching sessions:', error);
      setError('Failed to fetch sessions. Please try again later.');
    }
  };

  useEffect(() => {
    fetchSessions();
  }, []);

  const cancelSession = async (id) => {
    try {
      const response = await axios.put(`http://127.0.0.1:5000/api/sessions/${id}/cancel`);
      console.log('Cancel response:', response.data);
      // Refresh sessions to get updated booking statuses
      await fetchSessions();
    } catch (error) {
      console.error('Error cancelling session:', error.response?.data?.error || error.message);
      setError(error.response?.data?.error || 'Failed to cancel session. Please try again.');
    }
  };

  const startEditing = (session) => {
    setEditingSession(session.id);
    setFormData({
      client: session.client,
      date: session.date,
      time: session.time,
      status: session.status,
    });
  };

  const handleInputChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const updateSession = async (id) => {
    try {
      // Send data in the format expected by the backend
      const payload = {
        client: formData.client,
        date: formData.date,
        time: formData.time, // Expects HH:MM AM/PM (e.g., "10:00 AM")
        status: formData.status,
      };
      const response = await axios.put(`http://127.0.0.1:5000/api/sessions/${id}`, payload);
      console.log('Update response:', response.data);
      // Refresh sessions to get updated data
      await fetchSessions();
      setEditingSession(null);
      setFormData({ client: '', date: '', time: '', status: '' });
    } catch (error) {
      console.error('Error updating session:', error.response?.data?.error || error.message);
      setError(error.response?.data?.error || 'Failed to update session. Please try again.');
    }
  };

  const cancelEditing = () => {
    setEditingSession(null);
    setFormData({ client: '', date: '', time: '', status: '' });
  };

  const toggleUsers = (id) => {
    setShowUsers(showUsers === id ? null : id);
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('userId');
    localStorage.removeItem('role');
    navigate('/login');
  }

  return (
    <div className="min-h-screen bg-gray-100 p-6">
      <h1 className="text-3xl font-bold text-center mb-6">Facilitator Dashboard</h1>
      {error && <div className="text-red-600 text-center mb-4">{error}</div>}
      <div className="text-center mb-4">
        <button
          onClick={fetchSessions}
          className="bg-blue-500 text-white py-2 px-4 rounded hover:bg-blue-600"
        >
          Refresh Sessions
        </button>
      </div>
      <div className="text-center mb-4">
        <button
          onClick={handleLogout}
          className="bg-red-500 text-white py-2 px-4 rounded hover:bg-red-600"
        >
          Logout
        </button>
      </div>
      <div className="bg-white shadow-md rounded-lg overflow-hidden">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Client</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Date</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Time</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Facilitator</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Registered Users</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {sessions.map(session => (
              <tr key={session.id}>
                {editingSession === session.id ? (
                  <>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <input
                        type="text"
                        name="client"
                        value={formData.client}
                        onChange={handleInputChange}
                        className="border rounded p-1 w-full"
                      />
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <input
                        type="date"
                        name="date"
                        value={formData.date}
                        onChange={handleInputChange}
                        className="border rounded p-1 w-full"
                      />
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <input
                        type="time"
                        name="time"
                        value={formData.time}
                        onChange={handleInputChange}
                        className="border rounded p-1 w-full"
                        step="300" // 5-minute increments
                      />
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <select
                        name="status"
                        value={formData.status}
                        onChange={handleInputChange}
                        className="border rounded p-1 w-full"
                      >
                        <option value="Confirmed">Confirmed</option>
                        <option value="Pending">Pending</option>
                        <option value="Cancelled">Cancelled</option>
                      </select>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">{session.facilitator}</td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      {session.registeredUsers.join(', ')}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <button
                        onClick={() => updateSession(session.id)}
                        className="text-green-600 hover:text-green-900 mr-2"
                      >
                        Save
                      </button>
                      <button
                        onClick={cancelEditing}
                        className="text-red-600 hover:text-red-900"
                      >
                        Cancel
                      </button>
                    </td>
                  </>
                ) : (
                  <>
                    <td className="px-6 py-4 whitespace-nowrap">{session.client}</td>
                    <td className="px-6 py-4 whitespace-nowrap">{session.date}</td>
                    <td className="px-6 py-4 whitespace-nowrap">{session.time}</td>
                    <td className="px-6 py-4 whitespace-nowrap">{session.status}</td>
                    <td className="px-6 py-4 whitespace-nowrap">{session.facilitator}</td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <button
                        onClick={() => toggleUsers(session.id)}
                        className="text-blue-600 hover:text-blue-900"
                      >
                        {showUsers === session.id ? 'Hide Users' : 'Show Users'}
                      </button>
                      {showUsers === session.id && (
                        <ul className="mt-2 list-disc list-inside">
                          {session.registeredUsers.map((user, index) => (
                            <li key={index} className="text-sm">User ID: {user}</li>
                          ))}
                        </ul>
                      )}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <button
                        onClick={() => startEditing(session)}
                        className="text-blue-600 hover:text-blue-900 mr-2"
                      >
                        Edit
                      </button>
                      <button
                        onClick={() => cancelSession(session.id)}
                        className="text-red-600 hover:text-red-900"
                      >
                        Cancel Session
                      </button>
                    </td>
                  </>
                )}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default FacilitatorDashboard;