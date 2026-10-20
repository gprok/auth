from flask import Flask, render_template, request, flash, session, redirect
import sqlite3

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
app.secret_key = "kjadbhfkabkjdbkjabksdjbfdksjfbkjsdbfkdsj"


def get_db_conn():
    db = sqlite3.connect('data.db')
    db.row_factory = sqlite3.Row
    return db

def create_db():
    db = get_db_conn()
    db.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL, 
                    role TEXT
                 )
               """)
    db.commit()




@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.form 
        username = data['username']
        password = data['password']
        db = get_db_conn()
        user = db.execute("""
                            SELECT * FROM users 
                            WHERE username=? AND password=?
                          """, (username, password)).fetchone()
        if user:
            session['username'] = user['username']
            session['role'] = user['role']
            if user['role'] == 'admin':
                return redirect('/admin/panel')
            elif user['role'] == 'customer':
                return redirect('/customer/dashboard')
            else:
                flash("Unknown role, please login again")
                return render_template('login.html')
        else:
            flash("Invalid username/password")
            return render_template('login.html')
    else:
        return render_template('login.html')

@app.route('/admin/panel')
def admin_panel():
    if 'role' in session and session['role'] == 'admin':
        return render_template('admin.html')
    else: 
        flash("Invalid role for this page")
        return redirect('/login')

@app.route('/customer/dashboard')
def customer_dashboard():
    if 'role' in session and session['role'] == 'customer':
        return render_template('customer.html')
    else: 
        flash("Invalid role for this page")
        return redirect('/login')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


if __name__ == '__main__':
    create_db()
    app.run(debug=True)