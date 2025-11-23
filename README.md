# Car Price Prediction Web App

A fully functional Flask web application that uses machine learning to predict used car prices. Features include user authentication, prediction history tracking, and a modern car-themed UI.

link=https://motortrust.onrender.com/

## Features

- **User Authentication**: Secure signup and login with hashed passwords
- **ML Price Prediction**: Predict car prices based on multiple features
- **Prediction History**: Track and manage all your predictions
- **Modern UI**: Responsive car-themed design with Tailwind CSS
- **Dashboard**: View, filter, and delete past predictions
- **Secure Sessions**: Session-based authentication for protected routes

## Tech Stack

- **Backend**: Python, Flask
- **Database**: SQLite
- **ML**: scikit-learn
- **Frontend**: Jinja2 templates, Tailwind CSS
- **Security**: werkzeug password hashing, session management

## Project Structure

```
.
├── app.py                  # Main Flask application
├── create_model.py         # Script to create placeholder ML model
├── requirements.txt        # Python dependencies
├── database.db            # SQLite database (auto-created)
├── model.pkl              # Trained ML model (auto-created)
├── templates/             # HTML templates
│   ├── layout.html        # Base template with navigation
│   ├── index.html         # Home page with hero section
│   ├── login.html         # Login page
│   ├── signup.html        # Registration page
│   ├── predict.html       # Prediction form and results
│   ├── dashboard.html     # Prediction history table
│   └── about.html         # About page
└── static/
    └── css/
        └── style.css      # Custom styling

```

## Installation & Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Create the ML Model

Run the model creation script to generate a placeholder model:

```bash
python create_model.py
```

**Note**: For production use, replace `model.pkl` with a properly trained model using real car pricing data.

### 3. Set Environment Variable

The app uses the `SESSION_SECRET` environment variable for Flask's secret key. On Replit, this is automatically available.

For local development:
```bash
export SESSION_SECRET="your-secret-key-here"
```

### 4. Run the Application

```bash
python app.py
```

The app will be available at `http://0.0.0.0:5000`

## Usage

### First Time Setup

1. **Sign Up**: Create a new account with username, email, and password
2. **Login**: Use your credentials to access the application

### Making Predictions

1. Navigate to the **Predict** page
2. Fill in the car details:
   - Car Name (e.g., "Honda City")
   - Year of Purchase
   - Current Showroom Price (in ₹ Lakhs)
   - Kilometers Driven
   - Fuel Type (Petrol/Diesel/CNG)
   - Seller Type (Dealer/Individual)
   - Transmission (Manual/Automatic)
3. Click **Predict Price**
4. View the predicted selling price in Indian Rupees (₹)
5. Prediction is automatically saved to your dashboard

### Viewing History

1. Go to the **Dashboard** page
2. See all your past predictions in a sortable table
3. Delete unwanted predictions using the delete button

## Database Schema

### Users Table
- `id`: Primary key
- `username`: Unique username
- `email`: Unique email address
- `password_hash`: Hashed password
- `created_at`: Account creation timestamp

### Prediction History Table
- `id`: Primary key
- `user_id`: Foreign key to users table
- `car_name`: Name of the car
- `year`: Year of purchase
- `present_price`: Current showroom price
- `km_driven`: Total kilometers driven
- `fuel_type`: Type of fuel
- `seller_type`: Dealer or Individual
- `transmission`: Manual or Automatic
- `predicted_price`: ML predicted price
- `timestamp`: Prediction timestamp

## ML Model Features

The model uses the following features for prediction:
1. Present Price (current showroom price)
2. Kilometers Driven
3. Fuel Type (encoded)
4. Seller Type (encoded)
5. Transmission (encoded)
6. Age of Vehicle (calculated from year)

## Security Features

- Password hashing using werkzeug.security
- Session-based authentication
- Protected routes requiring login
- CSRF protection via Flask sessions
- Input validation and sanitization
- SQL injection prevention with parameterized queries

## Developer

**Bhavishya Katariya**
- Full-Stack Developer & ML Engineer
- Project: Car Price Prediction System

## Color Scheme

- **Primary**: Car Black (#1a1a1a)
- **Accent**: Car Red (#dc2626)
- **Text**: Car Grey (#9ca3af)

## Future Enhancements

- Add more sophisticated ML models
- Implement data visualization charts
- Add export functionality (CSV/PDF)
- Advanced filtering and search
- Price trend analysis
- Car comparison feature

## License

This project is for educational purposes.

---

Built with Flask, Tailwind CSS, and scikit-learn
# MotorTrust
