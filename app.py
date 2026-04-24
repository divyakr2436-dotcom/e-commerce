from flask import Flask, render_template, request, redirect, url_for import sqlite3

app = Flask(name)

Initialize database

conn = sqlite3.connect('shop.db') c = conn.cursor() c.execute('''CREATE TABLE IF NOT EXISTS products ( id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, price INTEGER, image TEXT )''') conn.commit() conn.close()

@app.route('/') def home(): conn = sqlite3.connect('shop.db') c = conn.cursor() c.execute('SELECT * FROM products') products = c.fetchall() conn.close() return render_template('home.html', products=products)

@app.route('/add', methods=['GET', 'POST']) def add_product(): if request.method == 'POST': name = request.form['name'] price = request.form['price'] image = request.form['image']

conn = sqlite3.connect('shop.db')
    c = conn.cursor()
    c.execute('INSERT INTO products (name, price, image) VALUES (?, ?, ?)', (name, price, image))
    conn.commit()
    conn.close()
    return redirect('/')
return render_template('add.html')

@app.route('/delete/int:id') def delete(id): conn = sqlite3.connect('shop.db') c = conn.cursor() c.execute('DELETE FROM products WHERE id=?', (id,)) conn.commit() conn.close() return redirect('/')

@app.route('/order/int:id') def order(id): conn = sqlite3.connect('shop.db') c = conn.cursor() c.execute('SELECT * FROM products WHERE id=?', (id,)) product = c.fetchone() conn.close()

message = f"I want to order {product[1]} for Rs {product[2]}"
phone = '91XXXXXXXXXX'  # Replace with shop number

return redirect(f"https://wa.me/{phone}?text={message}")

if name == 'main': app.run(debug=True)

---------- HTML FILES ----------

Create a folder called templates and add below files

home.html

"""

<!DOCTYPE html><html>
<head>
    <title>Food Shop</title>
</head>
<body>
    <h1>Food Menu</h1>
    <a href="/add">Add Product</a>
    <ul>
    {% for p in products %}
        <li>
            <img src="{{p[3]}}" width="100"><br>
            {{p[1]}} - ₹{{p[2]}}
            <br>
            <a href="/order/{{p[0]}}">Order</a>
            <a href="/delete/{{p[0]}}">Delete</a>
        </li>
    {% endfor %}
    </ul>
</body>
</html>
"""add.html

"""

<!DOCTYPE html><html>
<head>
    <title>Add Product</title>
</head>
<body>
    <h1>Add Food Item</h1>
    <form method="post">
        Name: <input type="text" name="name"><br>
        Price: <input type="number" name="price"><br>
        Image URL: <input type="text" name="image"><br>
        <button type="submit">Add</button>
    </form>
</body>
</html>
"""