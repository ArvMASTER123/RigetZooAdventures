from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask import Flask, render_template, url_for, redirect, request, jsonify
from datetime import datetime
from sqlalchemy import Column, Integer, DateTime, Boolean

from flask import Flask, render_template, url_for, redirect, request
from flask_login import UserMixin, LoginManager, login_user, logout_user, login_required
from flask_bcrypt import Bcrypt

#db = SQLAlchemy()
admin = Admin()
UPLOAD_FOLDER = 'static'
app = Flask(__name__, static_folder='static')
login_manager = LoginManager(app)
bcrypt = Bcrypt(app)

app.config['FLASK_ADMIN_SWATCH'] = "slate" #This is the admin tab colour
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/ArvinRangbar/Documents/RigetZooAdventures/DB Browser for SQLite/ZooAndHotel.db' #This is my SQLite database path
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

db = SQLAlchemy(app)
admin = Admin(app, name='Admin', template_mode='bootstrap3')

#User database column
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    email = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(100), nullable=False)

#Bookings database column
class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    datetime = db.Column(db.DateTime, nullable=False)
    adults = db.Column(db.Integer, nullable=False)
    children = db.Column(db.Integer, nullable=False)
    disabled = db.Column(db.Boolean, nullable=False)
    total_price = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"Ticket(date={self.date}, quantity={self.quantity}, disabled={self.disabled}, total_price={self.total_price})"

#Rooms database column
class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    checkin_date = db.Column(db.Date, nullable=False)
    checkout_date = db.Column(db.Date, nullable=False)
    adults = db.Column(db.Integer, nullable=False)
    children = db.Column(db.Integer, nullable=False)
    singleroom = db.Column(db.Integer, nullable=False)
    doubleroom = db.Column(db.Integer, nullable=False)
    disabled = db.Column(db.Boolean, nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    availability = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Room(date={self.name}, checkin_date={self.checkin_date}, checkout_date={self.checkout_date}, adults={self.adults} total_price={self.total_price})"

#Checkout database column
class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False)
    town = db.Column(db.String, nullable=False)
    postcode = db.Column(db.String, nullable=False)
    cardno = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f"Cart(fullname={self.fullname}, email={self.email}, address={self.address}, town={self.town}, postcode={self.postcode}, cardno{self.cardno})"

admin.add_view(ModelView(User, db.session)) #This is my User column for admin

admin.add_view(ModelView(Ticket, db.session)) #This is my Ticket column for admin

admin.add_view(ModelView(Room, db.session)) #This is Room column for admin

admin.add_view(ModelView(Cart, db.session)) #This is Cart column for admin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#app route for home page
@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

#app route for login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):  #Used bcrypt for password checking
            login_user(user)
            return redirect(url_for('homebookings'))  #Redirect to the appropriate route after login
    return render_template('login.html')

#app route for logging out 
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home')) #This will redirect it back to home page 

#app route for register page
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        if len(password) <= 8:
            error_message = 'Password must be more than 8 characters long'
            return render_template('register.html', error=error_message)
        hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

#app route for bookings page
@app.route('/homebookings')
def homebookings():
    return render_template('homebookings.html')

#app route for zoo bookings page
@app.route('/zoobookings', methods=['GET', 'POST'])
def zoobookings():
    if request.method == 'POST':
        date_str = request.form.get("checkin-datetime")
        date = datetime.strptime(date_str, '%Y-%m-%dT%H:%M')
        adults = float(request.form.get("adults-box"))
        children = float(request.form.get("children-box"))
        disabled = request.form.get("disabled-box")
        if disabled:
            disabled = False #If it's checked, set it to False
        else:
            disabled = True #If it's not checked, set it to True
        adult_price = float(18.35)
        child_price = float(12.75)
        total_price = float(adults * adult_price) + float(children * child_price) #Calculates the adults and child price to get total
        new_bookings = Ticket(datetime=date, adults=adults, children=children, disabled=disabled, total_price=total_price)
        db.session.add(new_bookings)
        db.session.commit()
        return redirect(url_for('checkout', zoo_price=total_price)) #Redirects to checkout page if successful
    else:
        return render_template('zoobookings.html')

#app route for hotel bookings page
@app.route('/hotelbookings', methods=['GET', 'POST'])
def hotelbookings():
    if request.method == 'POST':
        checkin_date_str = request.form.get("checkin-date")
        checkout_date_str = request.form.get("checkout-date")
        if not checkin_date_str or not checkout_date_str:
            # Handle case where date fields are empty
            return render_template('hotelbookings.html', error="Please provide both check-in and check-out dates.")
        checkin_date = datetime.strptime(checkin_date_str, '%Y-%m-%d')
        checkout_date = datetime.strptime(checkout_date_str, '%Y-%m-%d')
        adults = (request.form.get("adults-box"))
        children = (request.form.get("children-box"))
        singleroom = float(request.form.get("singleroom-box"))
        doubleroom = float(request.form.get("doubleroom-box"))
        disabled = request.form.get("disabled-box")
        if disabled:
            disabled = False # If it's checked, set it to False
        else:
            disabled = True # If it's not checked, set it to True
        singleroom_price = float(70.00)
        doubleroom_price = float(90.00)
        total_price = float(singleroom * singleroom_price) + float(doubleroom * doubleroom_price)
        availability = 300 #Availabilty starts at 300
        availability -= (singleroom + doubleroom)
        if availability >= 0:
            new_bookings = Room(checkin_date=checkin_date, checkout_date=checkout_date, adults=adults, children=children, singleroom=singleroom, doubleroom=doubleroom, disabled=disabled, total_price=total_price, availability=availability)
        db.session.add(new_bookings)
        db.session.commit()
        return redirect(url_for('checkout', hotel_price=total_price))
    else:
        return render_template('hotelbookings.html', error="Not enough availability. Please choose fewer rooms.")
#app route for hotel rooms page
@app.route('/hotelrooms')
def hotelrooms():
    return render_template('hotelrooms.html')

#app route for about us page
@app.route('/aboutus')
def aboutus():
    return render_template('aboutus.html')

#app route for contact us page
@app.route('/contact')
def contact():
    return render_template('contact.html')

#app route for education page
@app.route('/education')
def education():
    return render_template('education.html')

# app route for checkout page
@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'POST':
        fullname = request.form.get("firstname")
        email = request.form.get("email")
        address = request.form.get("address")
        town = request.form.get("town")
        postcode = request.form.get("postcode")
        cardno = request.form.get("cardnumber")
        # Retrieve prices from zoo and hotel 
        zoo_price = request.args.get('zoo_price')
        hotel_price = request.args.get('hotel_price')
        return redirect(url_for('receipt'))
    else:
        return render_template('checkout.html',  zoo_price=zoo_price, hotel_price=hotel_price)

#app route for receipt us page
@app.route('/receipt')
def receipt():
    return render_template('receipt.html')


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
