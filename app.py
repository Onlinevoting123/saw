from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

app.secret_key = 'Hemanth'

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name1 = db.Column(db.String(100), nullable=False)
    number1 = db.Column(db.Integer, nullable=False)
    address1 = db.Column(db.String(100), nullable=False)
    pincode1 = db.Column(db.Integer, nullable=False)
    names1 = db.Column(db.String(100), nullable=False)
    total1 = db.Column(db.Integer, nullable=False)

@app.route('/users', methods=['GET'])
def users_page():
    users = User.query.all() 
    return render_template('users.html', users=users)

products = [
    {'id': 1, 'name': 'Headphones', 'price': 999, 'image': '/static/images/beastheadphones.jpg'},
    {'id': 2, 'name': "Rudy's Shampoo", 'price': 129, 'image': '/static/images/rudyshampoo.jpg'},
    {'id': 3, 'name': 'OIG Handbag', 'price': 399, 'image': '/static/images/handbag.jpg'},
    {'id': 4, 'name': 'Alamy Bottle', 'price': 99, 'image': '/static/images/bottle.jpg'},
    {'id': 5, 'name': 'Luxury Lipstick', 'price': 129, 'image': '/static/images/luxurylipstick.avif'},
    {'id': 6, 'name': 'Mac Powder', 'price': 249, 'image': '/static/images/macpow.webp'},
    {'id': 7, 'name': 'Comb', 'price': 99, 'image': '/static/images/grooming.jpg'},
    {'id': 8, 'name': 'Teapot', 'price': 199, 'image': '/static/images/teapot.avif'},
    {'id': 9, 'name': 'Wrist Watch', 'price': 499, 'image': '/static/images/watch.jpg'},
    {'id': 10, 'name': 'JBL Speaker', 'price': 1999, 'image': '/static/images/jbl.avif'},
    {'id': 11, 'name': 'Nike Shoes', 'price': 899, 'image': '/static/images/nike.jpg'},
    {'id': 12, 'name': 'Table', 'price': 599, 'image': '/static/images/table.jpg'},
    {'id': 13, 'name': 'Sofaa', 'price': 2499, 'image': '/static/images/sofaa.webp'},
    {'id': 14, 'name': 'Bacardi Breezer', 'price': 199, 'image': '/static/images/breezer.jpg'},
    {'id': 15, 'name': "Victoria's Spray", 'price': 249, 'image': '/static/images/spray.jpg'},
    {'id': 16, 'name': 'Hair Strengthener', 'price': 149, 'image': '/static/images/strengthner.png'},
    {'id': 17, 'name': 'Hair Dryer', 'price': 699, 'image': '/static/images/hair.webp'},
    {'id': 18, 'name': 'Curlyhair Spray', 'price': 299, 'image': '/static/images/curlspray.jpg'},
]


@app.route('/')
def home():
    if 'customer_name' not in session or 'customer_number' not in session:
        return redirect(url_for('login'))
    return render_template('index.html', products=products)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['customer_name'] = request.form['customer_name']
        session['customer_number'] = request.form['customer_number']
        return redirect(url_for('home'))
    return render_template('login.html')


@app.route('/address', methods=['GET', 'POST'])
def address():
    if request.method == 'POST':
        session['customer_address'] = request.form['customer_address']
        session['customer_pincode'] = request.form['customer_pincode']
        return redirect(url_for('order'))
    return render_template('address.html')


@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out successfully!', 'success')
    return redirect(url_for('login'))


@app.route('/remove_from_cart/<int:product_id>', methods=['POST'])
def remove_from_cart(product_id):
    cart = session.get('cart', [])
    for item in cart:
        if item['id'] == product_id:
            item['quantity'] -= 1
            if item['quantity'] <= 0:
                cart.remove(item)
            break
    session['cart'] = cart 
    session.modified = True
    return redirect(url_for('view_cart'))


@app.route('/cart', methods=['GET'])
def view_cart():
    cart = session.get('cart', [])
    total = sum(item['price'] * item['quantity'] for item in cart)
    return render_template('try.html', cart=cart, total=total)


from flask import flash

@app.route('/add_to_cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    product = next((p for p in products if p['id'] == product_id), None)
    if product:
        cart = session.get('cart', [])
        cart_item = next((item for item in cart if item['id'] == product_id), None)
        if cart_item:
            cart_item['quantity'] += 1
        else:
            cart.append({'id': product['id'], 'name': product['name'], 'price': product['price'], 'quantity': 1})
        session['cart'] = cart
        flash(f"{product['name']} has been added to your cart!")
    else:
        flash("Product not found!", "error")
    return redirect(url_for('view_cart'))


@app.route('/order', methods=['POST', 'GET'])
def order():
    if 'cart' in session:
        order_history = session.get('order_history', [])
        total_price = sum(item['price'] * item['quantity'] for item in session['cart'])
        p=[]
        z=[]
        a=""
        for i in session['cart']:
            p.append(str(i['id']))
            p.append(i['name'])
            p.append(str(i['price']))
            p.append(str(i['quantity']))
            a=" ".join(p)
            z.append(a)
            p=[]
            a=""
        a="+".join(z)
        order_history.append({
            'order_id': len(order_history) + 1,
            'names': session['cart'],
            'total': total_price,
            'customer_name': session['customer_name'],
            'customer_number': session['customer_number'],
            'customer_address': session['customer_address'],
            'customer_pincode': session['customer_pincode'],
        })
        user_details = User(
            name1=session['customer_name'],
            number1=session['customer_number'],
            address1=session['customer_address'],
            pincode1=session['customer_pincode'],
            names1=a,
            total1=total_price
        )
        db.session.add(user_details)
        db.session.commit()
        session['order_history'] = order_history
        session.pop('cart', None)  
        session.modified = True
        flash('Your order has been placed successfully!', 'success')

    return render_template('order.html')


@app.route('/cart/history', methods=['GET'])
def order_history():
    orders = session.get('order_history', [])
    return render_template('history.html', orders=orders)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
