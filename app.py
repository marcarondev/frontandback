from flask import Flask, render_template, request, jsonify
import psycopg2
from werkzeug.security import generate_password_hash  # <-- Secure Passwords


# from flask_sqlalchemy import SQLAlchemy




app = Flask(__name__)

def get_db_connection():
    return psycopg2.connect(
        host="localhost",
        database="my_project",
        user="postgres",
        password="admin"
    )

@app.route('/home')
def home():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        firstName = request.form.get('firstName')
        lastName = request.form.get('lastName')
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        if not all([firstName, lastName, username, email, password]):
            return jsonify({"error": "All fields are required"}), 400

        hashed_password = generate_password_hash(password)  # <-- Secure password

        cur.execute('''
            INSERT INTO users (firstName, lastName, username, email, password) 
            VALUES (%s, %s, %s, %s, %s) RETURNING id
        ''', (firstName, lastName, username, email, hashed_password))

        conn.commit()
        cur.close()
        conn.close()

        return jsonify({"message": "User added successfully"}), 201
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500




if __name__ == '__main__':
    app.run(debug=True)