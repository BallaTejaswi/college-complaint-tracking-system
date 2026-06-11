from flask import Flask, render_template, request, session, redirect
import sqlite3

app = Flask(__name__)
app.secret_key = "college_project_secret"


@app.route('/')
def index():
    return redirect('/login')


@app.route('/home', methods=['GET', 'POST'])
def home():

    if 'user' not in session:
        return redirect('/login')

    if request.method == 'POST':

        name = session['user']
        category = request.form['category']
        description = request.form['description']

        conn = sqlite3.connect('complaints.db')
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO complaints(name, category, description, status) VALUES (?, ?, ?, ?)",
            (name, category, description, "Pending")
        )

        conn.commit()
        conn.close()

        return render_template(
    'home.html',
    message="Complaint Submitted Successfully"
)

    return render_template('home.html')


@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('complaints.db')
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO users(username, password, role) VALUES (?, ?, ?)",
            (username, password, "student")
        )

        conn.commit()
        conn.close()

        return redirect('/login')

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('complaints.db')
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (username, password)
        )

        user = cursor.fetchone()

        conn.close()

        if user:

            session['user'] = user[1]
            session['role'] = user[3]

            if user[3] == "admin":
                return redirect('/admin')

            return redirect('/home')

        return "Invalid Username or Password"

    return render_template('login.html')


@app.route('/admin')
def admin():

    if 'role' not in session or session['role'] != 'admin':
        return redirect('/login')

    conn = sqlite3.connect('complaints.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM complaints")
    complaints = cursor.fetchall()

    conn.close()

    return render_template('admin.html', complaints=complaints)


@app.route('/resolve/<int:id>')
def resolve(id):

    if 'role' not in session or session['role'] != 'admin':
        return redirect('/login')

    conn = sqlite3.connect('complaints.db')
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE complaints SET status='Resolved' WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect('/admin')


@app.route('/logout')
def logout():

    session.clear()
    return redirect('/login')


if __name__ == "__main__":
    app.run(debug=True)