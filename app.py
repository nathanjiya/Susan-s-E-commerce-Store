from flask import Flask, render_template, request, redirect, flash, url_for, session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Replace with a strong secret key

DB_NAME = 'users.db'

def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            )
        ''')
    print("Database initialized.")

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        full_name = request.form.get('full_name')
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if not all([full_name, email, username, password, confirm_password]):
            flash('All fields are required.', 'error')
            return redirect(url_for('signup'))

        if password != confirm_password:
            flash('Passwords do not match.', 'error')
            return redirect(url_for('signup'))

        hashed_password = generate_password_hash(password)

        try:
            with sqlite3.connect(DB_NAME) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO users (full_name, email, username, password) VALUES (?, ?, ?, ?)",
                    (full_name, email, username, hashed_password)
                )
                conn.commit()
            flash('Account created successfully!', 'success')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError as e:
            if 'email' in str(e):
                flash('Email already exists.', 'error')
            elif 'username' in str(e):
                flash('Username already exists.', 'error')
            else:
                flash('Something went wrong. Please try again.', 'error')
            return redirect(url_for('signup'))

    return render_template('sign-up.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')

        if not all([email, username, password]):
            flash('Please fill in all fields.', 'error')
            return redirect(url_for('login'))

        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE email=? AND username=?", (email, username))
            user = cursor.fetchone()

            if user and check_password_hash(user[4], password):
                session['user_id'] = user[0]
                session['username'] = user[3]
                session['email'] = user[2]
                session['is_admin'] = user[2] == 'jiyanndako@gmail.com'
                flash('Login successful!', 'success')
                return redirect(url_for('home'))
            else:
                flash('Invalid email, username, or password.', 'error')
                return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully.', 'success')
    return redirect(url_for('home'))


@app.route('/admin-dashboard')
def admin_dashboard():
    if not session.get('is_admin'):
        flash("Unauthorized access", "error")
        return redirect(url_for('home'))
    return render_template("admin-dashboard.html")


# Static Page Routes
@app.route('/index')
def shop():
    return render_template("index.html")

@app.route('/contact')
def contact():
    return render_template("contact.html")

@app.route('/cart')
def cart():
    return render_template("cart.html")

@app.route('/payment')
def payment():
    return render_template("payment.html")

@app.route('/male-shoe')
def men_shoes():
    return render_template("male-shoe.html")

@app.route('/female-shoe')
def women_shoes():
    return render_template("female-shoe.html")

@app.route('/female-shirts')
def female_shirts():
    return render_template("female-shirts.html")

@app.route('/men-shirt')
def men_shirt():
    return render_template("men-shirt.html")

@app.route('/trouser')
def trousers():
    return render_template("trouser.html")

@app.route('/male-accessories')
def men_accessories():
    return render_template("male-accessories.html")


# Product data mapping
products = {
    "female-shirt6": {
        "name": "Purple Shirt",
        "price": "N200",
        "image": "female shirt 6.jpeg"
    },
    "female-shirt5": {
        "name": "White shirt",
        "price": "N250",
        "image": "female shirt 5.jpeg"
    },
 "female-shirt4": {
        "name": "Black Shirt",
        "price": "N500",
        "image": "female shirt 4.jpeg"
    },
    "female-shirt3": {
        "name": "White shirt",
        "price": "N450",
        "image": "female shirt 3.jpeg"
    },
    "female-shirt2": {
        "name": "Red Shirt",
        "price": "N150",
        "image": "female shirt 2.jpeg"
    },
    "female-shirt1": {
        "name": "White shirt",
        "price": "N1200",
        "image": "female shirt 1.jpeg"
    },
    "female-shoe1":{
        "name": "White shoe",
        "price": "N1200",
        "image": "female shoe 1.jpeg"
    },
    "female-shoe2":{
        "name": "Pink shoe",
        "price": "N1200",
        "image": "female shoe 2.jpeg"
    },
    "female-shoe3":{
        "name": "Black and Gold shoe",
        "price": "N1200",
        "image": "female shoe 3.jpeg"
    },
    "female-shoe4":{
        "name": "Black hills",
        "price": "N1200",
        "image": "female shoe 4.jpeg"
    },
    "female-shoe5":{
        "name": "pink boots",
        "price": "N500",
        "image": "female shoe 5.jpeg"
    },
    "female-shoe6":{
        "name": "Nude hills",
        "price": "N500",
        "image": "female shoe 6.jpeg"
    },
    "male-accessories1": {
        "name": "Richard Mille Watch",
        "price": "₦1200",
        "image": "face cap.jpeg"
    },
    "male-accessories2": {
        "name": "Leather Belt",
        "price": "₦150",
        "image": "jean chain.jpeg"
    },
    "male-accessories3": {
        "name": "Blue Trainers",
        "price": "₦450",
        "image": "male accessories  2.jpeg"
    },
    "male-accessories4": {
        "name": "Men’s Shoes",
        "price": "₦500",
        "image": "male accessories 1.jpeg"
    },
    "male-accessories5": {
        "name": "Black Trouser",
        "price": "₦250",
        "image": "male accessories 3.jpeg"
    },
    "male-accessories6": {
        "name": "Black Shirt",
        "price": "₦200",
        "image": "male accessories 4.jpeg"
    },
    "male-shoes1": {
        "name": "Richard Mille Watch",
        "price": "₦1200",
        "image": "male shoes 1.jpeg"
    },
    "male-shoes2": {
        "name": "Leather Belt",
        "price": "₦150",
        "image": "male shoes 2.jpeg"
    },
    "male-shoes3": {
        "name": "Blue Trainers",
        "price": "₦450",
        "image": "male shoes 3.jpeg"
    },
    "male-shoes4": {
        "name": "Men’s Shoes",
        "price": "₦500",
        "image": "male shoes 4.jpeg"
    },
    "male-shoes5": {
        "name": "Black Trouser",
        "price": "₦250",
        "image": "male shoes 5.jpeg"
    },
    "male-shoes6": {
        "name": "Black Shirt",
        "price": "₦200",
        "image": "male shoes 6.jpeg"
    },
     "shirt1": {
        "name": "Richard Mille Watch",
        "price": "₦1200",
        "image": "shirt 1.jpeg"
    },
    "shirt2": {
        "name": "Leather Belt",
        "price": "₦150",
        "image": "shirt 2.jpeg"
    },
    "shirt3": {
        "name": "Blue Trainers",
        "price": "₦450",
        "image": "shirt 3.jpeg"
    },
    "shirt4": {
        "name": "Men’s Shoes",
        "price": "₦500",
        "image": "shirt 4.jpeg"
    },
    "shirt5": {
        "name": "Black Trouser",
        "price": "₦250",
        "image": "shirt 5.jpeg"
    },
    "shirt6": {
        "name": "Black Shirt",
        "price": "₦200",
        "image": "shirt 6.jpeg"
    },
    "trouser1": {
        "name": "Richard Mille Watch",
        "price": "₦1200",
        "image": "trouser 1.jpeg"
    },
    "trouser2": {
        "name": "Leather Belt",
        "price": "₦150",
        "image": "trouser 2.jpeg"
    },
    "trouser3": {
        "name": "Blue Trainers",
        "price": "₦450",
        "image": "trouser 3.jpeg"
    },
    "trouser4": {
        "name": "Men’s Shoes",
        "price": "₦500",
        "image": "trouser 4.jpeg"
    },
    "trouser5": {
        "name": "Black Trouser",
        "price": "₦250",
        "image": "trouser 5.jpeg"
    },
    "trouser6": {
        "name": "Black Shirt",
        "price": "₦200",
        "image": "trouser 6.jpeg"
    }
}

# Product route
@app.route('/<product_id>')
def product_page(product_id):
    product = products.get(product_id)
    if product:
        return render_template("product.html", product=product)
    return "Product not found", 404

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
