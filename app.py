# Importing flask module, render template which
# is used to render template files, request to read posted values.
from flask import (Flask, render_template, request, json, session,
                   url_for, flash)
from datetime import date
import sqlite3

# Creating app using flask, setting secret key for flask to encrypt password.
app = Flask(__name__)
app.secret_key = "ThisIsAndela"


# Define the basic route / and its corresponding request handler
@app.route("/")
@app.route("/main")
def main():
    return render_template('index.html')


# Define the route for submitting suggestions and rendering
@app.route('/writeSuggestion')
def write_suggestion():
    return render_template('writesuggestion.html')


# Define route for viewing suggestions and rendering
@app.route('/displaySuggestions', methods=['GET', 'POST'])
def display_suggestions():
    print request.form
    conn = sqlite3.connect('suggestbox.db')
    mycursor = conn.cursor()
    mycursor.execute('''SELECT post_title FROM suggestions
                     ORDER BY date_posted DESC''')
    title = list(mycursor.fetchall())
    mycursor.execute('''SELECT post_desc FROM suggestions
                     ORDER BY date_posted DESC''')
    content = list(mycursor.fetchall())
    mycursor.execute('''SELECT date_posted FROM suggestions
                     ORDER BY date_posted DESC''')
    date_posted = list(mycursor.fetchall())
    mycursor.execute('''SELECT author FROM suggestions
                     ORDER BY date_posted DESC''')
    author = list(mycursor.fetchall())
    mycursor.execute('''SELECT upvotes FROM suggestions
                     ORDER BY date_posted DESC''')
    upvotes = list(mycursor.fetchall())
    mycursor.execute('''SELECT downvotes FROM suggestions
                     ORDER BY date_posted DESC''')
    downvotes = list(mycursor.fetchall())
    mycursor.execute('''SELECT flag FROM suggestions
                     ORDER BY date_posted DESC''')
    flag = list(mycursor.fetchall())
    for item in title:
        print title, content, date_posted, author, upvotes, downvotes, flag
    mycursor.close()
    conn.close()
    return render_template('viewsuggestions.html')

# Define the route for posting suggestions and rendering
@app.route('/viewSuggestion',methods=['GET', 'POST'])
def view_suggestion():
    if request.method == "POST":
        print request.form
        conn = sqlite3.connect('suggestbox.db')
        mycursor = conn.cursor()
        mycursor.execute ('CREATE TABLE IF NOT EXISTS suggestions(post_id INTEGER PRIMARY KEY AUTOINCREMENT, post_title VARCHAR NOT NULL, post_desc VARCHAR NOT NULL, date_posted VARCHAR,	flag INT DEFAULT 0, upvotes INT DEFAULT 0, downvotes INT DEFAULT 0, author VARCHAR, FOREIGN KEY(author) REFERENCES users(user_email))')
        title = request.form['title']
        content = request.form['content']
        userId = session['username']
        today = date.today()
        mycursor.execute ('INSERT INTO suggestions (post_title, post_desc, date_posted, author) VALUES (?, ?, ?, ?)', (title, content, today, userId))
        conn.commit()
        mycursor.close()
        conn.close()
        return render_template('landingpage.html')
    elif 'username' in session:
        username = session['username']
        return render_template('landingpage.html')
    else:
        return render_template('signIn.html')

# Define the route for signup and render the signup page once the request
# comes to the route
@app.route("/showSignUp")
def signup():
    return render_template('signup.html')

# Define the route for landing page and render it. Post data to db.
@app.route("/showLanding", methods=["POST", "GET"])
def show_landing():
    # import pdb; pdb.set_trace()
    if request.method == "POST":
        #pass
        #return render_template('landingpage.html')
        conn = sqlite3.connect('suggestbox.db')
        mycursor = conn.cursor()
        mycursor.execute ('''CREATE TABLE IF NOT EXISTS
                          users(user_id BIGINT PRIMARY KEY, user_name VARCHAR,
                          user_email VARCHAR UNIQUE, user_username VARCHAR UNIQUE,
                          user_password VARCHAR) ''')
        inputName = request.form['inputName']
        inputEmail = request.form['inputEmail']
        inputUsername = request.form['inputUsername']
        inputPassword = request.form['inputPassword']
        mycursor.execute ("INSERT INTO users (user_name, user_email, user_username, user_password) VALUES (?, ?, ?, ?)", (inputName, inputEmail, inputUsername, inputPassword))
        conn.commit()
        session['username'] = inputEmail
        return render_template('Landingpage.html')
        mycursor.close()
        conn.close()
        #return render_template('Landingpage.html')
    elif 'username' in session:
        username = session['username']
        return render_template('Landingpage.html')
        return flash("Signed In")
    else:
        return render_template('signIn.html')

# Define the route for signin and render the signin page once the request
# comes to the route
@app.route("/showSignIn")
def signin():
    return render_template('signin.html')

# Define the route for login and render landingpage after successful login
@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        conn = sqlite3.connect('suggestbox.db')
        mycursor = conn.cursor()
        mycursor.execute('SELECT * FROM users WHERE user_email = ? AND user_password = ?', (request.form['inputEmail'], request.form['inputPassword']))
        if mycursor.fetchall():
            session['username'] = request.form['inputEmail']
            mycursor.close()
            conn.close()
            flash('Signed In')
            return render_template('landingpage.html')
        else:
            error = "Invalid credentials"
            return render_template('signin.html')
    return render_template('signin.html')

# Define route for logout. Remove the username from the session if it is there
@app.route('/logout')
def logout():
   session.pop('username', None)
   return render_template('index.html')

# Next, check if the executed file is the main program and run the app
if __name__ == "__main__":
    app.run(debug=True)
