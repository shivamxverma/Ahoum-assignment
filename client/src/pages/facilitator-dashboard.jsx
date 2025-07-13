import React, { useState, useEffect } from 'react';
import axios from 'axios';

// Mock API for sessions with registered users
const mockSessions = [
    {
        id: 1,
        client: "John Doe",
        date: "2025-07-15",
        time: "10:00 AM",
        status: "Confirmed",
        registeredUsers: ["Alice Smith", "Bob Johnson"]
    },
    {
        id: 2,
        client: "Jane Smith",
        date: "2025-07-16",
        time: "2:00 PM",
        status: "Pending",
        registeredUsers: ["Charlie Brown"]
    },
    {
        id: 3,
        client: "Alex Brown",
        date: "2025-07-17",
        time: "11:00 AM",
        status: "Confirmed",
        registeredUsers: ["David Lee", "Emma Wilson"]
    },
];

const FacilitatorDashboard = () => {
    const [sessions, setSessions] = useState([]);
    const [editingSession, setEditingSession] = useState(null);
    const [formData, setFormData] = useState({ client: "", date: "", time: "", status: "", registeredUsers: [] });
    const [showUsers, setShowUsers] = useState(null);

    // Fetch sessions (mock API call)
    useEffect(() => {
        setSessions(mockSessions);
    }, []);

    // Handle cancel session
    const cancelSession = (id) => {
        setSessions(sessions.map(session =>
            session.id === id ? { ...session, status: "Cancelled" } : session
        ));
    };

    // Handle edit session
    const startEditing = (session) => {
        setEditingSession(session.id);
        setFormData({
            client: session.client,
            date: session.date,
            time: session.time,
            status: session.status,
            registeredUsers: session.registeredUsers
        });
    };

    // Handle form input change
    const handleInputChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    // Handle update session
    const updateSession = (id) => {
        setSessions(sessions.map(session =>
            session.id === id ? { ...session, ...formData } : session
        ));
        setEditingSession(null);
        setFormData({ client: "", date: "", time: "", status: "", registeredUsers: [] });
    };

    // Cancel editing
    const cancelEditing = () => {
        setEditingSession(null);
        setFormData({ client: "", date: "", time: "", status: "", registeredUsers: [] });
    };

    // Toggle registered users visibility
    const toggleUsers = (id) => {
        setShowUsers(showUsers === id ? null : id);
    };

    return (
        <div className="min-h-screen bg-gray-100 p-6">
            <h1 className="text-3xl font-bold text-center mb-6">Facilitator Dashboard</h1>

            {/* Sessions Table */}
            <div className="bg-white shadow-md rounded-lg overflow-hidden">
                <table className="min-w-full divide-y divide-gray-200">
                    <thead className="bg-gray-50">
                        <tr>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Client</th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Date</th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Time</th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
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
                                        <td className="px-6 py-4 whitespace-nowrap">
                                            {formData.registeredUsers.join(", ")}
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
                                        <td className="px-6 py-4 whitespace-nowrap">
                                            <button
                                                onClick={() => toggleUsers(session.id)}
                                                className="text-blue-600 hover:text-blue-900"
                                            >
                                                {showUsers === session.id ? "Hide Users" : "Show Users"}
                                            </button>
                                            {showUsers === session.id && (
                                                <ul className="mt-2 list-disc list-inside">
                                                    {session.registeredUsers.map((user, index) => (
                                                        <li key={index} className="text-sm">{user}</li>
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