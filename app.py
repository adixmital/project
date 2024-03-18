from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# SQLite Database Configuration
DATABASE = 'shop.db'

def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

def get_db():
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    return db

@app.route('/')
def index():
    db = get_db()
    cursor = db.execute('SELECT * FROM products')
    products = cursor.fetchall()
    db.close()
    return render_template('index.html', products=products)

@app.route('/add_product', methods=['POST'])
def add_product():
    if request.method == 'POST':
        product_name = request.form['product_name']
        sale_price = float(request.form['sale_price'])
        cost_price = float(request.form['cost_price'])

        db = get_db()
        db.execute('INSERT INTO products (name, sale_price, cost_price) VALUES (?, ?, ?)',
                   [product_name, sale_price, cost_price])
        db.commit()
        db.close()
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
