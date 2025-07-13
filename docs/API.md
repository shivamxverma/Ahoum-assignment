# Event Management API

This document provides details on how to interact with the Event Management API, including endpoints for user registration, login, and bulk event insertion for testing purposes.

## Base URL
All API endpoints are relative to the base URL: `http://127.0.0.1:5000/api`

## Endpoints

### 1. Register
Register a new user account.

- **Method**: POST
- **Endpoint**: `/register`
- **Request Body**:
  ```json
  {
      "email": "shivam0xverma@gmail.com",
      "username": "shivamxverma",
      "password": "pass1232"
  }
  ```
- **Description**: Creates a new user with the provided email, username, and password.

### 2. Login
Authenticate a user to access the system.

- **Method**: POST
- **Endpoint**: `/login`
- **Request Body**:
  ```json
  {
      "email": "shivam0xverma@gmail.com",
      "username": "shivamxverma",
      "password": "pass1232"
  }
  ```
- **Description**: Authenticates a user with the provided credentials and returns a session token or similar authentication response.

### 3. Bulk Insert Events (Testing Purposes)
Insert multiple facilitators and events for testing the system.

- **Method**: POST
- **Endpoint**: `/bulkinsertevents`
- **Request Body**:
  ```json
  {
    "facilitators": [
      { "id": 1, "name": "Alice Smith", "email": "alice.smith@example.com", "phone": "1234567890" },
      { "id": 2, "name": "Bob Johnson", "email": "bob.johnson@example.com", "phone": "0987654321" },
      { "id": 3, "name": "Clara Lee", "email": "clara.lee@example.com", "phone": "5555555555" },
      { "id": 4, "name": "David Kim", "email": "david.kim@example.com", "phone": "1112223333" },
      { "id": 5, "name": "Emma Brown", "email": "emma.brown@example.com", "phone": "4445556666" },
      { "id": 6, "name": "Fiona Green", "email": "fiona.green@example.com", "phone": "7778889999" },
      { "id": 7, "name": "George Patel", "email": "george.patel@example.com", "phone": "2223334444" },
      { "id": 8, "name": "Hannah White", "email": "hannah.white@example.com", "phone": "6667778888" }
    ],
    "events": [
      {
        "id": 1,
        "name": "Yoga Retreat",
        "description": "A rejuvenating yoga retreat in the mountains.",
        "date": "2025-08-01T00:00:00",
        "location": "Mountain Resort, Himalayas",
        "sessions": [
          { "id": 101, "name": "Morning Yoga Flow", "start_time": "2025-08-01T09:00:00", "facilitator_id": 1 },
          { "id": 102, "name": "Evening Meditation", "start_time": "2025-08-01T18:00:00", "facilitator_id": 2 },
          { "id": 103, "name": "Sunset Yoga", "start_time": "2025-08-01T17:00:00", "facilitator_id": 3 }
        ]
      },
      {
        "id": 2,
        "name": "Meditation Workshop",
        "description": "Guided meditation for mindfulness and stress relief.",
        "date": "2025-07-10T00:00:00",
        "location": "Community Center, Delhi",
        "sessions": [
          { "id": 201, "name": "Morning Mindfulness", "start_time": "2025-07-10T10:00:00", "facilitator_id": 3 }
        ]
      },
      {
        "id": 3,
        "name": "Mindfulness Intensive",
        "description": "Deep dive into mindfulness techniques.",
        "date": "2025-07-20T00:00:00",
        "location": "City Hall, Mumbai",
        "sessions": [
          { "id": 301, "name": "Mindfulness Basics", "start_time": "2025-07-20T11:00:00", "facilitator_id": 1 },
          { "id": 302, "name": "Advanced Meditation", "start_time": "2025-07-20T14:00:00", "facilitator_id": 4 }
        ]
      },
      {
        "id": 4,
        "name": "Wellness Retreat",
        "description": "A holistic wellness experience with yoga and nutrition.",
        "date": "2025-08-15T00:00:00",
        "location": "Beach Resort, Goa",
        "sessions": [
          { "id": 401, "name": "Beach Yoga", "start_time": "2025-08-15T07:00:00", "facilitator_id": 5 },
          { "id": 402, "name": "Nutrition Workshop", "start_time": "2025-08-15T10:00:00", "facilitator_id": 6 }
        ]
      },
      {
        "id": 5,
        "name": "Breathwork Session",
        "description": "Learn breathwork techniques for relaxation.",
        "date": "2025-07-13T00:00:00",
        "location": "Yoga Studio, Bangalore",
        "sessions": [
          { "id": 501, "name": "Pranayama Basics", "start_time": "2025-07-13T09:00:00", "facilitator_id": 2 }
        ]
      },
      {
        "id": 6,
        "name": "Ayurveda Workshop",
        "description": "Explore Ayurvedic principles for health.",
        "date": "2025-08-10T00:00:00",
        "location": "Ayurveda Center, Kerala",
        "sessions": [
          { "id": 601, "name": "Ayurveda Intro", "start_time": "2025-08-10T10:00:00", "facilitator_id": 7 },
          { "id": 602, "name": "Herbal Remedies", "start_time": "2025-08-10T13:00:00", "facilitator_id": 8 },
          { "id": 603, "name": "Dietary Practices", "start_time": "2025-08-10T15:00:00", "facilitator_id": 7 }
        ]
      },
      {
        "id": 7,
        "name": "Tai Chi Retreat",
        "description": "A calming Tai Chi retreat for balance and harmony.",
        "date": "2025-09-01T00:00:00",
        "location": "Hill Station, Shimla",
        "sessions": [
          { "id": 701, "name": "Morning Tai Chi", "start_time": "2025-09-01T06:00:00", "facilitator_id": 4 }
        ]
      },
      {
        "id": 8,
        "name": "Sound Healing Session",
        "description": "Experience the power of sound therapy.",
        "date": "2025-07-05T00:00:00",
        "location": "Wellness Center, Chennai",
        "sessions": [
          { "id": 801, "name": "Gong Bath", "start_time": "2025-07-05T18:00:00", "facilitator_id": 5 },
          { "id": 802, "name": "Tibetan Bowls", "start_time": "2025-07-05T20:00:00", "facilitator_id": 6 }
        ]
      },
      {
        "id": 9,
        "name": "Reiki Workshop",
        "description": "Learn the basics of Reiki healing.",
        "date": "2025-08-20T00:00:00",
        "location": "Healing Space, Pune",
        "sessions": [
          { "id": 901, "name": "Reiki Level 1", "start_time": "2025-08-20T10:00:00", "facilitator_id": 3 },
          { "id": 902, "name": "Reiki Practice", "start_time": "2025-08-20T14:00:00", "facilitator_id": 3 }
        ]
      },
      {
        "id": 10,
        "name": "Stress Management Seminar",
        "description": "Techniques to manage stress effectively.",
        "date": "2025-07-12T00:00:00",
        "location": "Conference Hall, Hyderabad",
        "sessions": [
          { "id": 1001, "name": "Stress Relief Techniques", "start_time": "2025-07-12T11:00:00", "facilitator_id": 8 }
        ]
      }
    ]
  }
  ```# 🧘 Booking System for Sessions & Retreats



