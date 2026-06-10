from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():

    if request.method == 'POST':

        name = request.form['name']
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

    return render_template('home.html')


@app.route('/admin')
def admin():

    conn = sqlite3.connect('complaints.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM complaints")
    complaints = cursor.fetchall()

    conn.close()

    return render_template('admin.html', complaints=complaints)


@app.route('/resolve/<int:id>')
def resolve(id):

    conn = sqlite3.connect('complaints.db')
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE complaints SET status='Resolved' WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return admin()


if __name__ == "__main__":
    app.run(debug=True)