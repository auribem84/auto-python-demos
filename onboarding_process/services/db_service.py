import psycopg2
from config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD

def create_customer(customer_name, email):
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO customers (name, email, created_at)
        VALUES (%s, %s, NOW())
        RETURNING id;
    """, (customer_name, email))

    customer_id = cur.fetchone()[0]

    conn.commit()
    cur.close()
    conn.close()

    return customer_id