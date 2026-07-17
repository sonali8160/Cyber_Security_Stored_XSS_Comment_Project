from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Create database table
def init_db():
    conn = sqlite3.connect('comments.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS comments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            comment TEXT
        )
    ''')

    conn.commit()
    conn.close()

init_db()

@app.route('/', methods=['GET', 'POST'])
def index():

    if request.method == 'POST':

        comment = request.form['comment']

        # Store comment in database
        conn = sqlite3.connect('comments.db')
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO comments (comment) VALUES (?)",
            (comment,)
        )

        conn.commit()
        conn.close()

        return redirect('/')

    # Fetch comments
    conn = sqlite3.connect('comments.db')
    cursor = conn.cursor()

    cursor.execute("SELECT comment FROM comments")

    comments = cursor.fetchall()

    conn.close()

    return render_template('index.html', comments=comments)

if __name__ == '__main__':
    app.run(debug=True)