# WorkoutBuddy API

A comprehensive FastAPI-based backend service for managing workout routines, diet plans, and fitness progress tracking. This API provides endpoints for user authentication, workout management, diet planning, progress tracking, and AI-powered fitness insights.

## 🚀 Features

- **User Authentication & Authorization**
  - JWT-based authentication
  - OAuth integration (Google, GitHub)
  - Password reset functionality
  - API key management

- **Workout Management**
  - Create and manage workout routines
  - Track workout progress and performance
  - Generate workout charts and analytics
  - Exercise library with detailed information

- **Diet Planning**
  - Create personalized diet plans
  - Track daily meal logs
  - Monitor nutritional intake
  - Diet progress tracking

- **AI Integration**
  - AI-powered workout recommendations
  - Smart diet suggestions
  - Progress insights using Gemini AI
  - Chatbot for fitness queries

- **Progress Analytics**
  - Visual progress charts
  - Performance metrics
  - Historical data tracking

## 🛠️ Tech Stack

- **Framework**: FastAPI (Python)
- **Database**: MongoDB
- **Authentication**: JWT, OAuth2
- **AI Services**: Google Gemini, Groq
- **Email Service**: SMTP integration
- **Testing**: pytest
- **Documentation**: Auto-generated OpenAPI/Swagger

## 📋 Prerequisites

- Python 3.8+
- MongoDB 4.4+
- Redis (for caching)
- Google/Github OAuth credentials (for OAuth)
- Gemini API key (for AI features)

## 🔧 Installation

### 1. Clone the repository
```bash
git clone <repository-url>
cd WBBackend
```

### 2. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment setup
Create a `.env` file in the root directory:
```env
# MongoDB
MONGO_URL=mongodb://localhost:27017
DB_NAME=workoutbuddy

# JWT
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=120

# OAuth
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
SESSION_SECRET_KEY=your-session-secret

# Email
MAILTRAP_HOST=sandbox.smtp.mailtrap.io
MAILTRAP_PORT=587
MAILTRAP_USERNAME=your-username
MAILTRAP_PASSWORD=your-password
FROM_EMAIL=noreply@workoutbuddy.com

# AI Services
GROQ_API_KEY=your-groq-api-key
```

### 5. Run the application
```bash
# Development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Production server
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## 📖 API Documentation

Once the server is running, you can access:
- **Interactive API Docs**: http://localhost:8000/docs
- **ReDoc Documentation**: http://localhost:8000/redoc
- **OpenAPI Schema**: http://localhost:8000/openapi.json

## 🔑 Authentication

### JWT Token Authentication
```bash
# Login to get access token
POST /api/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123"
}

# Use token in subsequent requests
Authorization: Bearer <your-jwt-token>
```

### OAuth Authentication
- **Google OAuth**: `/api/oauth/google`
- **GitHub OAuth**: `/api/oauth/github`

## 📊 API Endpoints Overview

### Authentication
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `POST /api/auth/logout` - User logout
- `POST /api/auth/forgot-password` - Password reset request
- `POST /api/auth/reset-password` - Password reset confirmation

### Users
- `GET /api/users/me` - Get current user profile
- `PUT /api/users/me` - Update user profile
- `DELETE /api/users/me` - Delete user account

### Workouts
- `GET /api/workouts` - Get all workouts
- `POST /api/workouts` - Create new workout
- `GET /api/workouts/{workout_id}` - Get specific workout
- `PUT /api/workouts/{workout_id}` - Update workout
- `DELETE /api/workouts/{workout_id}` - Delete workout
- `POST /api/workouts/{workout_id}/progress` - Add workout progress

### Diet Plans
- `GET /api/diet-plans` - Get all diet plans
- `POST /api/diet-plans` - Create new diet plan
- `GET /api/diet-plans/{plan_id}` - Get specific diet plan
- `PUT /api/diet-plans/{plan_id}` - Update diet plan
- `DELETE /api/diet-plans/{plan_id}` - Delete diet plan

### Meal Logs
- `GET /api/progress/meal-logs` - Get meal logs
- `POST /api/progress/meal-logs` - Create meal log
- `PUT /api/progress/meal-logs/{log_id}` - Update meal log
- `DELETE /api/progress/meal-logs/{log_id}` - Delete meal log

### Progress Tracking
- `GET /api/progress/workout` - Get workout progress
- `GET /api/progress/diet` - Get diet progress
- `GET /api/progress/charts` - Get progress charts
- `GET /api/progress/workout-charts` - Get workout analytics

### AI Features
- `POST /api/chat` - Chat with fitness AI assistant
- `GET /api/chat/recommendations` - Get AI workout/diet recommendations

## 🧪 Testing

Run the test suite:
```bash
pytest app/tests/ -v
```

## 🐳 Docker Support

### Using Docker Compose
```bash
# Build and run
docker-compose up --build

# Run in background
docker-compose up -d
```

## 📁 Project Structure

```
WBBackend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application entry point
│   ├── config/
│   │   ├── __init__.py
│   │   └── settings.py         # Configuration settings
│   ├── api/
│   │   ├── __init__.py
│   │   ├── api_v1.py           # Main API router
│   │   └── routes/             # API endpoints
│   │       ├── auth.py         # Authentication endpoints
│   │       ├── users.py        # User management
│   │       ├── workout.py      # Workout endpoints
│   │       ├── diet.py         # Diet plan endpoints
│   │       ├── chat.py         # AI chatbot
│   │       └── oauth.py        # OAuth integration
│   ├── db/
│   │   ├── __init__.py
│   │   └── mongodb.py          # MongoDB connection
│   ├── models/                 # Database models
│   ├── schemas/                # Pydantic schemas
│   ├── utils/                  # Utility functions
│   └── tests/                  # Test files
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

For support, email support@workoutbuddy.com or join our Slack channel.

## 🙏 Acknowledgments

- FastAPI team for the amazing framework
- MongoDB for the flexible database
- Google for Gemini AI integration
- All contributors and testers
