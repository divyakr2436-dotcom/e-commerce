from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Initialize database
conn = sqlite3.connect('shop.db')
c = conn.cursor()

c.execute('''
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    price INTEGER,
    image TEXT
)
''')

conn.commit()
conn.close()


# Home page
@app.route('/')
def home():
    conn = sqlite3.connect('shop.db')
    c = conn.cursor()

    c.execute('SELECT * FROM products')
    products = c.fetchall()

    conn.close()
    return render_template('home.html', products=products)


# Add product
@app.route('/add', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        image = request.form['image']

        conn = sqlite3.connect('shop.db')
        c = conn.cursor()

        c.execute(
            'INSERT INTO products (name, price, image) VALUES (?, ?, ?)',
            (name, price, image)
        )

        conn.commit()
        conn.close()

        return redirect('/')

    return render_template('add.html')


# Delete product
@app.route('/delete/<int:id>')
def delete(id):
    conn = sqlite3.connect('shop.db')
    c = conn.cursor()

    c.execute('DELETE FROM products WHERE id = ?', (id,))

    conn.commit()
    conn.close()

    return redirect('/')


# Order via WhatsApp
@app.route('/order/<int:id>')
def order(id):
    conn = sqlite3.connect('shop.db')
    c = conn.cursor()

    c.execute('SELECT * FROM products WHERE id = ?', (id,))
    product = c.fetchone()

    conn.close()

    message = f"I want to order {product[1]} for Rs {product[2]}"
    phone = '8951024306'  # Replace with shop owner's number

    return redirect(f"https://wa.me/{phone}?text={message}")


# Run app
if __name__ == '__main__':
    app.run(debug=True)



