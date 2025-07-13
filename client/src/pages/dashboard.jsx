import React, { useState ,useEffect} from 'react';
import axios from 'axios';

function Dashboard() {
  const [Booking, setIsSessionBooked] = useState(false);
  const [events, setEvents] = useState([]);
  const [filter, setFilter] = useState("all");

  useEffect(() => {
    const fetchEvents = async () => {
      try {
        const response = await axios.get("http://127.0.0.1:5000/api/events");
        setEvents(response.data);
      } catch (error) {
        console.error("Error fetching events:", error);
      }
    };

    fetchEvents();
  }, []);

  const currentDate = new Date("2025-07-13");

  const filteredEvents = events.filter(event => {
    const eventDate = new Date(event.date);
    if (filter === "past") return eventDate < currentDate;
    if (filter === "present") return eventDate.toDateString() === currentDate.toDateString();
    if (filter === "upcoming") return eventDate > currentDate;
    return true;
  });



  const handleBookSession = async (sessionId) => {
    try {
      const response = await axios.post(`http://127.0.0.1:5000/api/events/book`, {
        userId: 2,
        sessionId: sessionId,
      });
      if (response.status === 200) {
        alert("Session booked successfully!");
        setIsSessionBooked(true);
      } else {
        alert("Failed to book session.");
      }
    } catch (error) {
      console.error("Booking error:", error);
      alert("Error booking session.");
    }
  };

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-3xl font-bold mb-4">Event Dashboard</h1>
      
      <div className="mb-4">
        <button
          className={`mr-2 px-4 py-2 rounded ${filter === "all" ? "bg-blue-500 text-white" : "bg-gray-200"}`}
          onClick={() => setFilter("all")}
        >
          All
        </button>
        <button
          className={`mr-2 px-4 py-2 rounded ${filter === "past" ? "bg-blue-500 text-white" : "bg-gray-200"}`}
          onClick={() => setFilter("past")}
        >
          Past
        </button>
        <button
          className={`mr-2 px-4 py-2 rounded ${filter === "present" ? "bg-blue-500 text-white" : "bg-gray-200"}`}
          onClick={() => setFilter("present")}
        >
          Present
        </button>
        <button
          className={`px-4 py-2 rounded ${filter === "upcoming" ? "bg-blue-500 text-white" : "bg-gray-200"}`}
          onClick={() => setFilter("upcoming")}
        >
          Upcoming
        </button>
      </div>

      <div className="grid gap-4">
        {filteredEvents.map(event => {
          const eventDate = new Date(event.date);
          const isPastEvent = eventDate < currentDate;

          return (
            <div key={event.id} className="border p-4 rounded shadow">
              <h2 className="text-xl font-semibold">{event.title}</h2>
              <p>{event.description}</p>
              <p className="text-gray-600">Date: {event.date}</p>
              <h3 className="mt-2 font-medium">Sessions:</h3>
              <ul className="list-disc pl-5">
                {event.sessions.map(session => (
                  <li key={session.id} className="mt-1">
                    {new Date(session.time).toLocaleString()} - Facilitator: {session.facilitator.name}
                    {!isPastEvent && (
                      <button
                        className="ml-4 px-3 py-1 bg-green-500 text-white rounded hover:bg-green-600"
                        onClick={() => handleBookSession(session.id)}
                      >
                        {Booking ? "Booked" : "Book Session"}
                      </button>
                    )}
                  </li>
                ))}
              </ul>
            </div>
          );
        })}
      </div>
    </div>
  );
}

export default Dashboard;