# Importing flask module, render template which is used to render template files,
# request to read posted values
from flask import Flask, render_template, request, json, session, redirect, url_for, escape, abort, flash
from datetime import datetime
import sqlite3

# Creating app using flask
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

# Define the route for viewing suggestions and rendering
@app.route('/viewSuggestion')
def view_suggestion():
    if request.method == "POST":
        conn = sqlite3.connect('suggestbox.db')
        mycursor = conn.cursor()

        mycursor.execute ('CREATE TABLE IF NOT EXISTS suggestions(post_id BIGINT PRIMARY KEY, post_title VARCHAR, post_desc VARCHAR, date VARCHAR, flag INT, upvotes INT, downvotes INT, user_id BIGINT, FOREIGN KEY(user_id) REFERENCES users(user_id) )')
        title = request.form['title']
        content = request.form['content']
        date = datetime(year='YYYY', month='mm', day='dd')
        mycursor.execute ("INSERT INTO suggestions (post_title, post_desc, date) VALUES (?, ?, ?)", (title, content, date))
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

        mycursor.execute ('CREATE TABLE IF NOT EXISTS users(user_id BIGINT PRIMARY KEY, user_name VARCHAR, user_email VARCHAR UNIQUE, user_username VARCHAR UNIQUE, user_password VARCHAR) ')
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
        #return 'Logged in as ' + username + '<br>' + \
        #"<b><a href = '/logout'>click here to log out</a></b>"
    else:
        return render_template('signIn.html')


# Define the route for signin and render the signup page once the request
# comes to the route
@app.route("/showSignIn")
def signin():
    return render_template('signin.html')

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
           return render_template('Landingpage.html')
       else:
           flash('Sign In Unsuccessful, Try Again')
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
