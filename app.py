from flask import Flask, render_template, request, redirect
import sqlite3, re

app = Flask(__name__)

# Database helper
def get_db_connection():
    conn = sqlite3.connect('contacts.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    contacts = conn.execute('SELECT * FROM contacts').fetchall()
    conn.close()
    return render_template('index.html', contacts=contacts)

@app.route('/add', methods=('GET', 'POST'))
def add():
    if request.method == 'POST':
        fname = request.form['first_name']
        lname = request.form['last_name']
        address = request.form['address']
        email = request.form['email']
        phone = request.form['phone']

        # Email validation
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return "Invalid email format"

        conn = get_db_connection()
        try:
            conn.execute("INSERT INTO contacts (first_name, last_name, address, email, phone) VALUES (?, ?, ?, ?, ?)",
                         (fname, lname, address, email, phone))
            conn.commit()
        except sqlite3.IntegrityError:
            return "Email already exists!"
        finally:
            conn.close()
        return redirect('/')
    return render_template('add.html')

@app.route('/edit/<int:id>', methods=('GET', 'POST'))
def edit(id):
    conn = get_db_connection()
    contact = conn.execute('SELECT * FROM contacts WHERE id = ?', (id,)).fetchone()

    if request.method == 'POST':
        fname = request.form['first_name']
        lname = request.form['last_name']
        address = request.form['address']
        email = request.form['email']
        phone = request.form['phone']

        conn.execute('UPDATE contacts SET first_name=?, last_name=?, address=?, email=?, phone=? WHERE id=?',
                     (fname, lname, address, email, phone, id))
        conn.commit()
        conn.close()
        return redirect('/')
    conn.close()
    return render_template('edit.html', contact=contact)

@app.route('/delete/<int:id>')
def delete(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM contacts WHERE id=?', (id,))
    conn.commit()
    conn.close()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
