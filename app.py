from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# Thiết lập kết nối cơ sở dữ liệu
db = mysql.connector.connect(
    host="ballast.proxy.rlwy.net",
    port=58123,
    user="root",
    password="GBPCDocCJnhHBEsnYjiseNfjKKzcOnWJ",
    database="railway"
)
cursor = db.cursor()

@app.route('/', methods=['GET'])
def index():
    search_query = request.args.get('search', '')  # Lấy từ khóa tìm kiếm từ URL
    if search_query:
        # Truy vấn tìm kiếm trong cơ sở dữ liệu theo tên sản phẩm
        cursor.execute('SELECT * FROM products WHERE name LIKE %s', ('%' + search_query + '%',))
    else:
        # Nếu không có từ khóa tìm kiếm, lấy tất cả sản phẩm
        cursor.execute('SELECT * FROM products')
    
    products = cursor.fetchall()
    return render_template('index.html', products=products, search_query=search_query)


@app.route('/add', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = request.form['price']
        
        cursor.execute('INSERT INTO products (name, description, price) VALUES (%s, %s, %s)', (name, description, price))
        db.commit()
        return redirect(url_for('index'))
    return render_template('add_product.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_product(id):
    cursor.execute('SELECT * FROM products WHERE id = %s', (id,))
    product = cursor.fetchone()

    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = request.form['price']
        
        cursor.execute('UPDATE products SET name = %s, description = %s, price = %s WHERE id = %s',
                       (name, description, price, id))
        db.commit()
        return redirect(url_for('index'))
    
    return render_template('edit_product.html', product=product)

@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete_product(id):
    cursor.execute('SELECT * FROM products WHERE id = %s', (id,))
    product = cursor.fetchone()

    if request.method == 'POST':
        cursor.execute('DELETE FROM products WHERE id = %s', (id,))
        db.commit()
        return redirect(url_for('index'))

    return render_template('delete_product.html', product=product)

if __name__ == '__main__':
    app.run(debug=True)
