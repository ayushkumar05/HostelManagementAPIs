
from flask import Flask, request, render_template, redirect, session,jsonify
import sqlite3
from flask_cors import CORS
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "secret_key_for_session"

# connect to database
conn = sqlite3.connect("hosteldatabase.db")
cursor = conn.cursor()

# create table if it doesn't exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT NOT NULL,
    password TEXT NOT NULL,
    role INTEGER NOT NULL
);
""")
conn.commit()
conn.close()
CORS(app)


# signup route
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        conn = sqlite3.connect("hosteldatabase.db")
        cursor = conn.cursor()
        # get user data
        data = request.get_json()
        print('data')
        email = data['email']
        password = data['password']
        role = data['role']
        # hash password
        hashed_password = generate_password_hash(password)

        # insert user data into the database
        cursor.execute("""
        INSERT INTO users (email, password,role)
        VALUES (?, ?, ?);
        """, (email, hashed_password,role))
        conn.commit()
        conn.close()
        # redirect to login page
        return 'yay'
    return render_template("signup.html")

# login route
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        print('POST SUCCESS')
        conn = sqlite3.connect("hosteldatabase.db")
        cursor = conn.cursor()
        # get user data
        data = request.get_json()
        email = data['email']
        password = data['password']
        # get user by email
        cursor.execute("""
        SELECT * FROM users WHERE email=?;
        """, (email,))
        user = cursor.fetchone()
        conn.commit()
        conn.close()
        # check if the user exists
        if user:
            # check if the password is correct
            if check_password_hash(user[2], password):
                # set user_id in session
                session["user_id"] = user[0]
                # redirect to dashboard
                return str(user)
        # return error message if the user does not exist or the password is incorrect
        return "Incorrect Email or Password"
    return 'login'

#apis to return data
def get_all_female():
    conn = sqlite3.connect('hosteldatabase.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM students where "gender"=="F"')
    rows = cursor.fetchall()
    conn.close()
    return jsonify(rows)
    
def get_all_male():
    conn = sqlite3.connect('hosteldatabase.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM students where "gender"=="M"')
    rows = cursor.fetchall()
    conn.close()
    return jsonify(rows)

def get_all():
    conn = sqlite3.connect('hosteldatabase.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM students')
    rows = cursor.fetchall()
    conn.close()
    return jsonify(rows)

@app.route('/UserData', methods = ['GET'])
def users():
    if "user_id" in session:
        cursor.execute("""
        SELECT role FROM users WHERE id=?;
""", (session["user_id"],))
        g = cursor.fetchone()
        if g== 1:
            return get_all_female()
        elif g==2:
            return get_all_male()
        elif g == 3:
            return get_all()
    else:
        return jsonify({'error': 'Invalid user'})

#print(get_all_male())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)