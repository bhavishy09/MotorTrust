import os
import sqlite3
import pickle
from datetime import datetime
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import numpy as np

app = Flask(__name__)
app.secret_key = os.environ.get('SESSION_SECRET', 'dev-secret-key-change-in-production')

DATABASE = 'database.db'
MODEL_PATH = 'model.pkl'

def get_db():
    conn = sqlite3.connect(DATABASE, timeout=10.0)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS prediction_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            car_name TEXT NOT NULL,
            year INTEGER NOT NULL,
            present_price REAL NOT NULL,
            km_driven INTEGER NOT NULL,
            fuel_type TEXT NOT NULL,
            seller_type TEXT NOT NULL,
            transmission TEXT NOT NULL,
            predicted_price REAL NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    conn.commit()
    conn.close()

def load_model():
    try:
        if os.path.exists(MODEL_PATH):
            with open(MODEL_PATH, 'rb') as f:
                return pickle.load(f)
        else:
            return None
    except Exception as e:
        print(f"Error loading model: {e}")
        return None

model = load_model()

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login to access this page.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        
        if not username or not email or not password:
            flash('All fields are required.', 'error')
            return render_template('signup.html')
        
        if password != confirm_password:
            flash('Passwords do not match.', 'error')
            return render_template('signup.html')
        
        if len(password) < 6:
            flash('Password must be at least 6 characters long.', 'error')
            return render_template('signup.html')
        
        try:
            conn = get_db()
            password_hash = generate_password_hash(password)
            conn.execute(
                'INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)',
                (username, email, password_hash)
            )
            conn.commit()
            conn.close()
            flash('Account created successfully! Please login.', 'success')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Username or email already exists.', 'error')
            return render_template('signup.html')
    
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        
        if not username or not password:
            flash('Username and password are required.', 'error')
            return render_template('login.html')
        
        conn = get_db()
        user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        conn.close()
        
        if user and check_password_hash(user['password_hash'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            flash(f'Welcome back, {user["username"]}!', 'success')
            return redirect(url_for('predict'))
        else:
            flash('Invalid username or password.', 'error')
            return render_template('login.html')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out successfully.', 'success')
    return redirect(url_for('index'))

@app.route('/predict', methods=['GET', 'POST'])
@login_required
def predict():
    if request.method == 'POST':
        try:
            car_name = request.form.get('car_name', '').strip()
            year = int(request.form.get('year', 0))
            present_price = float(request.form.get('present_price', 0))
            km_driven = int(request.form.get('km_driven', 0))
            fuel_type = request.form.get('fuel_type', '')
            seller_type = request.form.get('seller_type', '')
            transmission = request.form.get('transmission', '')
            
            if not car_name or year < 1900 or present_price <= 0 or km_driven < 0:
                flash('Please provide valid input values.', 'error')
                return render_template('predict.html')
            
            if model is None:
                predicted_price = present_price * 0.65
            else:
                fuel_encoded = 1 if fuel_type == 'Petrol' else 0
                seller_encoded = 1 if seller_type == 'Individual' else 0
                transmission_encoded = 1 if transmission == 'Manual' else 0
                current_year = datetime.now().year
                years_old = current_year - year
                
                features = np.array([[present_price, km_driven, fuel_encoded, 
                                    seller_encoded, transmission_encoded, years_old]])
                predicted_price = float(model.predict(features)[0])
            
            conn = get_db()
            conn.execute('''
                INSERT INTO prediction_history 
                (user_id, car_name, year, present_price, km_driven, fuel_type, 
                 seller_type, transmission, predicted_price)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (session['user_id'], car_name, year, present_price, km_driven,
                  fuel_type, seller_type, transmission, predicted_price))
            conn.commit()
            conn.close()
            
            return render_template('predict.html', 
                                 prediction=predicted_price,
                                 car_name=car_name,
                                 year=year,
                                 present_price=present_price,
                                 km_driven=km_driven,
                                 fuel_type=fuel_type,
                                 seller_type=seller_type,
                                 transmission=transmission)
        
        except ValueError:
            flash('Invalid input. Please check your values.', 'error')
            return render_template('predict.html')
        except Exception as e:
            flash(f'An error occurred: {str(e)}', 'error')
            return render_template('predict.html')
    
    return render_template('predict.html')

@app.route('/dashboard')
@login_required
def dashboard():
    conn = get_db()
    predictions = conn.execute('''
        SELECT * FROM prediction_history 
        WHERE user_id = ? 
        ORDER BY timestamp DESC
    ''', (session['user_id'],)).fetchall()
    conn.close()
    
    return render_template('dashboard.html', predictions=predictions)

@app.route('/delete_prediction/<int:prediction_id>', methods=['POST'])
@login_required
def delete_prediction(prediction_id):
    conn = get_db()
    conn.execute('''
        DELETE FROM prediction_history 
        WHERE id = ? AND user_id = ?
    ''', (prediction_id, session['user_id']))
    conn.commit()
    conn.close()
    
    flash('Prediction deleted successfully.', 'success')
    return redirect(url_for('dashboard'))

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
