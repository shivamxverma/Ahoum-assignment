import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

const api = axios.create({
  baseURL: 'http://127.0.0.1:5000/api', 
  headers: {
    'Content-Type': 'application/json',
  },
});

function Dashboard() {
  const [bookings, setBookings] = useState([]);
  const [events, setEvents] = useState([]);
  const [filter, setFilter] = useState('upcoming');
  const navigate = useNavigate();

  useEffect(() => {
    const fetchEventsAndBookings = async () => {
      try {
        const [eventsResponse, bookingsResponse] = await Promise.all([
          axios.get('http://127.0.0.1:5000/api/events'),
          axios.get('http://127.0.0.1:5000/api/bookings')
        ]);
        setEvents(eventsResponse.data);
        setBookings(bookingsResponse.data);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    fetchEventsAndBookings();
  }, []);

  const currentDate = new Date();

  const filteredEvents = events.filter(event => {
    const eventDate = new Date(event.date);
    return eventDate >= currentDate; 
  });

  const filteredBookings = bookings.filter(booking => {
    const bookingDate = new Date(booking.event.date);
    if (filter === 'past') return bookingDate < currentDate;
    if (filter === 'present') return bookingDate.toDateString() === currentDate.toDateString();
    if (filter === 'upcoming') return bookingDate > currentDate;
    return true;
  });

  const handleBookSession = async (sessionId, eventId) => {
    try {
      const response = await axios.post(
        'http://127.0.0.1:5000/api/events/book',
        {
          userId: localStorage.getItem('userId'),
          sessionId: sessionId,
          eventId: eventId
        },
        { headers: { Authorization: `Bearer ${localStorage.getItem('token')}` } }
      );
      if (response.status === 200) {
        alert('Session booked successfully!');
        setBookings([...bookings, response.data.booking]);
      } else {
        alert('Failed to book session.');
      }
    } catch (error) {
      console.error('Booking error:', error);
      alert('Error booking session.');
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('userId');
    localStorage.removeItem('role');
    navigate('/login');
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-50 to-purple-50 p-6">
      <div className="container mx-auto">
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-4xl font-extrabold text-gray-900">Event Dashboard</h1>
          <button
            onClick={handleLogout}
            className="bg-red-600 text-white py-2 px-6 rounded-lg hover:bg-red-700 transition duration-200"
          >
            Logout
          </button>
        </div>

        {/* Bookable Events Section */}
        <div className="mb-12">
          <h2 className="text-2xl font-bold text-gray-800 mb-6">Bookable Events</h2>
          <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
            {filteredEvents.length === 0 && (
              <p className="text-gray-600 col-span-full">No upcoming events available.</p>
            )}
            {filteredEvents.map(event => (
              <div
                key={event.id}
                className="bg-white p-6 rounded-xl shadow-lg hover:shadow-xl transition duration-300"
              >
                <h3 className="text-xl font-semibold text-gray-900">{event.title}</h3>
                <p className="text-gray-600 mt-2">{event.description}</p>
                <p className="text-gray-500 mt-1">Date: {new Date(event.date).toLocaleDateString()}</p>
                <h4 className="mt-4 font-medium text-gray-700">Sessions:</h4>
                <ul className="mt-2 space-y-2">
                  {event.sessions.map(session => {
                    const isBooked = bookings.some(
                      booking => booking.sessionId === session.id && booking.eventId === event.id
                    );
                    return (
                      <li key={session.id} className="flex items-center justify-between">
                        <span>
                          {new Date(session.time).toLocaleString()} - Facilitator: {session.facilitator.name}
                        </span>
                        {isBooked ? (
                          <span className="text-green-600 font-medium">Booked</span>
                        ) : (
                          <button
                            onClick={() => handleBookSession(session.id, event.id)}
                            className="ml-4 bg-indigo-600 text-white py-1 px-3 rounded-lg hover:bg-indigo-700 transition duration-200"
                          >
                            Book Session
                          </button>
                        )}
                      </li>
                    );
                  })}
                </ul>
              </div>
            ))}
          </div>
        </div>

        {/* User's Bookings Section */}
        <div>
          <h2 className="text-2xl font-bold text-gray-800 mb-6">Your Bookings</h2>
          <div className="flex space-x-4 mb-6">
            <button
              className={`px-4 py-2 rounded-lg ${
                filter === 'all' ? 'bg-indigo-600 text-white' : 'bg-gray-200 text-gray-700'
              } hover:bg-indigo-500 hover:text-white transition duration-200`}
              onClick={() => setFilter('all')}
            >
              All
            </button>
            <button
              className={`px-4 py-2 rounded-lg ${
                filter === 'past' ? 'bg-indigo-600 text-white' : 'bg-gray-200 text-gray-700'
              } hover:bg-indigo-500 hover:text-white transition duration-200`}
              onClick={() => setFilter('past')}
            >
              Past
            </button>
            <button
              className={`px-4 py-2 rounded-lg ${
                filter === 'present' ? 'bg-indigo-600 text-white' : 'bg-gray-200 text-gray-700'
              } hover:bg-indigo-500 hover:text-white transition duration-200`}
              onClick={() => setFilter('present')}
            >
              Present
            </button>
            <button
              className={`px-4 py-2 rounded-lg ${
                filter === 'upcoming' ? 'bg-indigo-600 text-white' : 'bg-gray-200 text-gray-700'
              } hover:bg-indigo-500 hover:text-white transition duration-200`}
              onClick={() => setFilter('upcoming')}
            >
              Upcoming
            </button>
          </div>
          <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
            {filteredBookings.length === 0 && (
              <p className="text-gray-600 col-span-full">No bookings found for this filter.</p>
            )}
            {filteredBookings.map(booking => (
              <div
                key={booking.id}
                className="bg-white p-6 rounded-xl shadow-lg hover:shadow-xl transition duration-300"
              >
                <h3 className="text-xl font-semibold text-gray-900">{booking.event.title}</h3>
                <p className="text-gray-600 mt-2">{booking.event.description}</p>
                <p className="text-gray-500 mt-1">
                  Date: {new Date(booking.event.date).toLocaleDateString()}
                </p>
                <p className="text-gray-500 mt-1">
                  Session: {new Date(booking.session.time).toLocaleString()} - Facilitator:{' '}
                  {booking.session.facilitator.name}
                </p>
                <p className="text-green-600 mt-2 font-medium">Booked</p>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

export default Dashboard;