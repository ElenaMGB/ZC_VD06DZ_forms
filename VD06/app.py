from flask import Flask, render_template, request
import sqlite3
from datetime import datetime

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users
        (id INTEGER PRIMARY KEY AUTOINCREMENT,
         name TEXT NOT NULL,
         city TEXT NOT NULL,
         hobby TEXT NOT NULL,
         age INTEGER NOT NULL,
         created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)
    ''')
    conn.commit()
    conn.close()

def get_users():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('SELECT * FROM users ORDER BY created_at DESC')
    users = []
    for row in c.fetchall():
        users.append({
            'id': row[0],
            'name': row[1],
            'city': row[2],
            'hobby': row[3],
            'age': row[4],
            'created_at': row[5]
        })
    conn.close()
    return users

def add_user(user_data):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO users (name, city, hobby, age)
        VALUES (?, ?, ?, ?)
    ''', (user_data['name'], user_data['city'], user_data['hobby'], user_data['age']))
    conn.commit()
    conn.close()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_data = {
            'name': request.form.get('name'),
            'city': request.form.get('city'),
            'hobby': request.form.get('hobby'),
            'age': request.form.get('age')
        }
        add_user(user_data)
    
    users = get_users()
    return render_template('index.html', users=users)

if __name__ == '__main__':
    init_db()
    app.run(debug=False)