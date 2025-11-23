import sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash, session
import re
from backend.db_connection import DatabaseConnection
from backend.observer import Subject, UserObserver

# ----------------------------
# Step 1: Initialize database
# ----------------------------
def init_db():
    db = DatabaseConnection()
    c = db.get_cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS contact(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fname TEXT NOT NULL,
            lname TEXT NOT NULL,
            email TEXT NOT NULL,
            message TEXT NOT NULL
        )
    ''')
    db.commit()
    db.close()

init_db()  # Ensure database exists before app starts

# ----------------------------
# Flask app setup
# ----------------------------
app = Flask(__name__)
app.secret_key = "supersecretkey"  # Needed for session & flash messages

# ----------------------------
# Create a Subject (represents the Recipe Manager)
# ----------------------------
recipe_subject = Subject()
from backend.observer import AdminObserver

admin = AdminObserver("Admin")
recipe_subject.add_observer(admin)

# Example: predefined followers (these could be users later)
user1 = UserObserver("Aymah")
user2 = UserObserver("Mubashra")
admin =AdminObserver("admin")
# Add them as observers
recipe_subject.add_observer(user1)
recipe_subject.add_observer(user2)
recipe_subject.add_observer(admin)

# ----------------------------
# Signup route
# ----------------------------
@app.route('/signup', methods=['GET', 'POST'])
def signup_page():
    if request.method == 'POST':
        name = request.form['name'].strip()
        email = request.form['email'].strip()
        password = request.form['password'].strip()

        # Backend validation
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-z]{2,}$'
        password_pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&]).{6,}$'

        if not re.match(email_pattern, email):
            flash("❌ Invalid email format!", "error")
            return redirect(url_for('signup_page'))
        if not re.match(password_pattern, password):
            flash("❌ Password must have uppercase, lowercase, number & special char!", "error")
            return redirect(url_for('signup_page'))

        # Save to database
        db = DatabaseConnection()
        c = db.get_cursor()
        try:
            c.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)", (name, email, password))
            db.commit()

            # Notify all observers (Observer Pattern)
            recipe_subject.notify_observers(f"New user joined: {name}")

            # Auto-login after signup
            session['user'] = name
            return redirect(url_for('dashboard'))

        except sqlite3.IntegrityError:
            flash("❌ Email already exists!", "error")
            return redirect(url_for('signup_page'))
        

    return render_template('signup.html')

# ----------------------------
# Login route
# ----------------------------
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email'].strip()
        password = request.form['password'].strip()

        # Backend validation
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-z]{2,}$'
        password_pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&]).{6,}$'

        if not re.match(email_pattern, email) or not re.match(password_pattern, password):
            flash("❌ Invalid email or password format!", "error")
            return redirect(url_for('login'))

        # Check credentials in database
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("SELECT name FROM users WHERE email=? AND password=?", (email, password))
        user = c.fetchone()
        conn.close()

        if user:
            session['user'] = user[0]  # Store user name in session
            return redirect(url_for('dashboard'))
        else:
            flash("❌ Invalid credentials!", "error")
            return redirect(url_for('login'))

    return render_template('login.html')

# ----------------------------
# Dashboard route (protected)
# ----------------------------
@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))
    name = session['user']

    # Collect all observer notifications
    notifications = []

    return render_template('index.html', name=name, notifications=notifications)

# ----------------------------
# Logout route
# ----------------------------
@app.route('/contact', methods=['GET', 'POST'])
def contact_page():
    if request.method == 'POST':
        fname = request.form['fname'].strip()
        lname = request.form['lname'].strip()
        email = request.form['email'].strip()
        message = request.form['message'].strip()

        # Save to database
        db = DatabaseConnection()
        c = db.get_cursor()
        c.execute("INSERT INTO contact(fname, lname, email, message) VALUES (?, ?, ?, ?)",
                  (fname, lname, email, message))
        db.commit()
        flash("Message sent successfully")
        return redirect(url_for('contact_page'))

    return render_template('contact.html')
@app.route('/logout')
def logout():
    session.pop('user', None)
    flash("✅ Logged out successfully!", "success")
    return redirect(url_for('login'))

@app.route('/home')
def home():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('index.html')


@app.route('/diet')
def diet():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('diet.html')


@app.route('/contact')
def contact():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('contact.html')

@app.route('/admin')
def admin_dashboard():
    return render_template('admin.html', notifications=admin.notifications)
# ----------------------------
# Run app
# ----------------------------
if __name__ == '__main__':
    app.run(debug=True)