from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
import os

app = Flask(__name__)

# Hàm tạo kết nối mới đến DB
def get_db_connection():
    return mysql.connector.connect(
        host=os.environ.get("DB_HOST"),
        user=os.environ.get("DB_USER"),
        password=os.environ.get("DB_PASSWORD"),
        database=os.environ.get("DB_NAME"),
        port=int(os.environ.get("DB_PORT", 3306))
    )

@app.route('/', methods=['GET'])
def index():
    search_query = request.args.get('search', '')
    db = get_db_connection()
    cursor = db.cursor()
    
    if search_query:
        cursor.execute('SELECT * FROM products WHERE name LIKE %s', ('%' + search_query + '%',))
    else:
        cursor.execute('SELECT * FROM products')
    
    products = cursor.fetchall()
    cursor.close()
    db.close()
    
    return render_template('index.html', products=products, search_query=search_query)

@app.route('/add', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = request.form['price']

        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute('INSERT INTO products (name, description, price) VALUES (%s, %s, %s)', (name, description, price))
        db.commit()
        cursor.close()
        db.close()

        return redirect(url_for('index'))
    return render_template('add_product.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_product(id):
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM products WHERE id = %s', (id,))
    product = cursor.fetchone()

    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = request.form['price']

        cursor.execute('UPDATE products SET name = %s, description = %s, price = %s WHERE id = %s',
                       (name, description, price, id))
        db.commit()
        cursor.close()
        db.close()
        return redirect(url_for('index'))

    cursor.close()
    db.close()
    return render_template('edit_product.html', product=product)

@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete_product(id):
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM products WHERE id = %s', (id,))
    product = cursor.fetchone()

    if request.method == 'POST':
        cursor.execute('DELETE FROM products WHERE id = %s', (id,))
        db.commit()
        cursor.close()
        db.close()
        return redirect(url_for('index'))

    cursor.close()
    db.close()
    return render_template('delete_product.html', product=product)
