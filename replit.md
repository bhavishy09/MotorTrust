# Car Price Prediction Web App

## Project Overview
A Flask-based web application that uses machine learning to predict used car prices. The app features user authentication, ML model integration, prediction history tracking, and a modern car-themed responsive UI.

## Recent Changes (November 16, 2024)
- Created complete Flask web application from scratch
- Implemented user authentication system with secure password hashing
- Built SQLite database schema for users and prediction history
- Integrated ML model (scikit-learn) for car price predictions
- Created responsive car-themed UI with Tailwind CSS
- Added all required pages: Home, Login, Signup, Predict, Dashboard, About
- Implemented prediction history management with delete functionality
- Set up workflow to run Flask app on port 5000

## Project Architecture

### Backend (Flask)
- **app.py**: Main Flask application with routes and business logic
- **Database**: SQLite with two tables (users, prediction_history)
- **ML Model**: scikit-learn Linear Regression model (model.pkl)
- **Authentication**: Session-based auth with werkzeug password hashing
- **Security**: Protected routes, input validation, SQL injection prevention

### Frontend (Templates)
- **layout.html**: Base template with navigation and footer
- **index.html**: Home page with hero section and features
- **login.html / signup.html**: Authentication forms
- **predict.html**: Car price prediction form and results display
- **dashboard.html**: Prediction history table with delete functionality
- **about.html**: Project and developer information

### Styling
- **Tailwind CSS**: Via CDN for rapid development
- **Custom CSS**: Car-themed styles in static/css/style.css
- **Color Scheme**: Black (#1a1a1a), Red (#dc2626), Grey (#9ca3af)

## Key Features
1. **User Authentication**: Signup, login, logout with session management
2. **ML Predictions**: Uses 6 features (price, mileage, fuel, seller, transmission, age)
3. **Prediction History**: Automatic saving and dashboard display
4. **Responsive Design**: Works on desktop, tablet, and mobile
5. **Input Validation**: Client and server-side validation
6. **Error Handling**: User-friendly error messages

## Database Schema

### Users Table
- id (PRIMARY KEY)
- username (UNIQUE)
- email (UNIQUE)
- password_hash
- created_at

### Prediction History Table
- id (PRIMARY KEY)
- user_id (FOREIGN KEY)
- car_name, year, present_price, km_driven
- fuel_type, seller_type, transmission
- predicted_price
- timestamp

## Running the Application
- Workflow: `python app.py`
- Port: 5000
- Access: http://0.0.0.0:5000

## Dependencies
- Flask 3.0.0
- werkzeug 3.0.1
- scikit-learn 1.3.2
- numpy 1.24.3
- pandas 2.0.3
- python-dotenv 1.0.0

## Environment Variables
- SESSION_SECRET: Used for Flask session encryption

## Developer
Bhavishya Katariya - Full-Stack Developer & ML Engineer
