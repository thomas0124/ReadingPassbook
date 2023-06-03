from flask import Flask, render_template, request, redirect, session
import sqlite3
from helpers import apology
from werkzeug.security import check_password_hash, generate_password_hash


db = sqlite3.connect('book.db', check_same_thread=False)
app = Flask(__name__)

app.secret_key = 'your_secret_key'

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Log user in"""
    # Forget any user_id
    session.clear()
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", (request.form.get("username"),))
        result = rows.fetchall()
        print(result)

        # Ensure username exists and password is correct
        if len(result) != 1 or not check_password_hash(result[0][1], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = result[0][0]
        # Redirect user to home page
        return redirect("/")
    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out"""
    # Forget any user_id
    session.clear()
    # Redirect user to login form
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirm = request.form.get("confirmation")
        if not username:
            return apology("missing username", 400)
        if not password:
            return apology("missing password", 400)
        if not confirm:
            return apology("missing confirmation", 400)
        if len(password) < 8:
            return apology("password must be 8 charaters long", 400)
        if not any(char.isupper() for char in password):
            return apology("You must include a capital letter", 400)
        if not any(char.isdigit() for char in password):
            return apology("You must include  a number", 400)
        if password == confirm:
            pass_tmp = password
        else:
            return apology("Password don't match", 400)
        hash = generate_password_hash(request.form.get("password"))
        rows = db.execute("SELECT * FROM users WHERE username = ?", (username,))
        if len(rows.fetchall()) == 0:
            username = request.form.get("username")
            db.execute("INSERT INTO users (username, user_password) VALUES(?, ?)", (username, hash,))
            return redirect("/")
        else:
            return apology("Usename already exists. Enter a new username!!", 400)
    else:
        return render_template("register.html")

@app.route("/confirm", methods=["GET", "POST"])
def confirm():
    return render_template("confirm.html", price=100)
if __name__ == '__main__':
    app.run(port=8000, debug=True)