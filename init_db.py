import mysql.connector

db = mysql.connector.connect(
    host="ballast.proxy.rlwy.net",
    port=58123,
    user="root",
    password="GBPCDocCJnhHBEsnYjiseNfjKKzcOnWJ",
    database="railway"
)

cursor = db.cursor()

cursor.execute("DROP TABLE IF EXISTS products")  # 👈 Dòng này sẽ xóa bảng cũ

cursor.execute("""
CREATE TABLE products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price FLOAT NOT NULL
)
""")

db.commit()
db.close()
