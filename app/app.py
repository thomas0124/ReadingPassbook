from flask import Flask, render_template, request, redirect, session
import sqlite3
from helpers import apology
from werkzeug.security import check_password_hash, generate_password_hash
import os
import cv2
from pyzbar import pyzbar
import requests

db = sqlite3.connect('book.db', check_same_thread=False)
db.execute("PRAGMA foreign_keys = ON")
app = Flask(__name__)

app.secret_key = 'your_secret_key'

@app.route('/')
def index():
    if 'user_id' not in session:
        return render_template("index.html", price=0)
    user_id = session['user_id']
    price = db.execute("SELECT SUM(price) FROM books WHERE user_id = ?", (user_id,))
    return render_template("index.html", price=price.fetchall()[0][0])

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
        if len(result) != 1 or not check_password_hash(result[0][2], request.form.get("password")):
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
            db.execute("INSERT INTO users (username, password) VALUES(?, ?)", (username, hash,))
            db.commit()
            return redirect("/")
        else:
            return apology("Usename already exists. Enter a new username!!", 400)
    else:
        return render_template("register.html")


@app.route("/confirm", methods=["GET", "POST"])
def confirm():
    if 'user_id' not in session:
        return redirect("/")
    user_id = session['user_id']
    if request.method == 'POST':
        file = request.files['file']
        image_filename = file.filename
        file.save(os.path.join('./static/image', image_filename))
        image_path = os.path.join('./static/image', image_filename)

        # バーコードを読み取る
        barcodes = read_barcode(image_path)

        if len(barcodes) > 0:
            for barcode in barcodes:
                # 本の価格と名前を取得する
                price, name = get_book_price(barcode)
                print(f"名前: {name}")
                print(f"価格: {price}円")
        else:
            print("バーコードが検出されませんでした。")
        db.execute("INSERT INTO books (title, price, user_id) VALUES (?, ?, ?)", (name, price, user_id,))
        db.commit()
        return render_template("confirm.html", image_filename=image_filename, item_price=price, item_name=name)
    else:
        return render_template("confirm.html", item_price=None, item_name=None)

def read_barcode(image_path):
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    barcodes = pyzbar.decode(gray)

    barcode_data = []
    for barcode in barcodes:
        barcode_data.append(barcode.data.decode('utf-8'))

    return barcode_data

def get_book_price(barcode):
    # 楽天商品検索API (BooksGenre/Search/)のURL
    url = "https://app.rakuten.co.jp/services/api/IchibaItem/Search/20170706"

    # URLのパラメータ
    params = {
        # 取得したアプリIDを設定する
        "applicationId" : "1044852592706171326",
        "keyword" : barcode,
        "format" : "json"
    }

    # APIを実行して結果を取得する
    result = requests.get(url, params=params)

    # jsonにデコードする
    json_result = result.json()

    # 結果から本の情報を取得する
    if "Items" in json_result and len(json_result["Items"]) > 0:
        item = json_result["Items"][0]["Item"]
        item_name = item["itemName"]
        item_price = item["itemPrice"]
        return item_price, item_name
    else:
        return None, None


if __name__ == '__main__':
    app.run(port=8000, debug=True)
