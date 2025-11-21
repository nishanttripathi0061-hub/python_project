from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# In-memory product list
products = []

@app.route('/')
def home():
    return render_template('index.html', products=products)


@app.route('/add', methods=['POST'])
def add_product():
    pid = request.form.get('id', '').strip()
    name = request.form.get('name', '').strip()
    price = request.form.get('price', '').strip()
    quantity = request.form.get('quantity', '').strip()

    # Validation
    if not pid or not name:
        return render_template('index.html', products=products)

    # Convert price
    if price.replace('.', '', 1).isdigit():
        price_val = float(price)
    else:
        price_val = price

    # Convert quantity
    if quantity.isdigit():
        qty_val = int(quantity)
    else:
        qty_val = quantity

    # Add product
    new_product = {
        'product_id': pid,
        'name': name,
        'price': price_val,
        'quantity': qty_val
    }

    products.append(new_product)
    return redirect(url_for('home'))


@app.route('/delete/<pid>')
def delete_product(pid):
    global products
    products = [p for p in products if p['product_id'] != pid]
    return redirect(url_for('home'))


@app.route('/update/<pid>', methods=['POST'])
def update_product(pid):
    name = request.form.get('name', '').strip()
    price = request.form.get('price', '').strip()
    quantity = request.form.get('quantity', '').strip()

    for p in products:
        if p['product_id'] == pid:
            if name:
                p['name'] = name
            if price.replace('.', '', 1).isdigit():
                p['price'] = float(price)
            else:
                p['price'] = price
            if quantity.isdigit():
                p['quantity'] = int(quantity)
            else:
                p['quantity'] = quantity
            break

    return redirect(url_for('home'))


@app.route('/search', methods=['POST'])
def search_product():
    term = request.form.get('term', '').strip().lower()
    if not term:
        return redirect(url_for('home'))

    result = [p for p in products if term in str(p.get('product_id', '')).lower() or term in str(p.get('name', '')).lower()]
    return render_template('index.html', products=result)


if __name__ == '__main__':
    app.run(debug=True)
