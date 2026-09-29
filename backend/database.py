import sqlite3
import os
from datetime import datetime


DATABASE_FOLDER = "database"
DATABASE_PATH = os.path.join(
    DATABASE_FOLDER,
    "products.db"
)


def get_connection():

    os.makedirs(
        DATABASE_FOLDER,
        exist_ok=True
    )

    connection = sqlite3.connect(
        DATABASE_PATH
    )

    connection.row_factory = sqlite3.Row

    return connection


def initialize_database():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            url TEXT NOT NULL,

            title TEXT,

            price TEXT,

            price_value REAL,

            rating TEXT,

            review_count TEXT,

            availability TEXT,

            image TEXT,

            scraped_at TEXT NOT NULL

        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reviews (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            product_url TEXT NOT NULL,

            reviewer TEXT,

            rating TEXT,

            title TEXT,

            review_text TEXT,

            review_date TEXT,

            scraped_at TEXT NOT NULL

        )
    """)

    connection.commit()

    connection.close()


def save_product(product):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO products (

            url,
            title,
            price,
            price_value,
            rating,
            review_count,
            availability,
            image,
            scraped_at

        )

        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)

    """, (

        product["url"],
        product["title"],
        product["price"],
        product["price_value"],
        product["rating"],
        product["reviews"],
        product["availability"],
        product["image"],
        datetime.now().isoformat()

    ))

    connection.commit()

    connection.close()


def save_reviews(
    product_url,
    reviews
):

    connection = get_connection()

    cursor = connection.cursor()

    for review in reviews:

        cursor.execute("""
            INSERT INTO reviews (

                product_url,
                reviewer,
                rating,
                title,
                review_text,
                review_date,
                scraped_at

            )

            VALUES (?, ?, ?, ?, ?, ?, ?)

        """, (

            product_url,
            review["reviewer"],
            review["rating"],
            review["title"],
            review["text"],
            review["date"],
            datetime.now().isoformat()

        ))

    connection.commit()

    connection.close()


def get_price_history(url):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            scraped_at,
            price_value

        FROM products

        WHERE url = ?

        AND price_value IS NOT NULL

        ORDER BY scraped_at ASC

    """, (url,))

    rows = cursor.fetchall()

    connection.close()

    return [

        {
            "date": row["scraped_at"],
            "price": row["price_value"]
        }

        for row in rows
    ]


def get_reviews(url):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        SELECT

            reviewer,
            rating,
            title,
            review_text,
            review_date

        FROM reviews

        WHERE product_url = ?

        ORDER BY id DESC

        LIMIT 20

    """, (url,))

    rows = cursor.fetchall()

    connection.close()

    return [

        {
            "reviewer": row["reviewer"],
            "rating": row["rating"],
            "title": row["title"],
            "text": row["review_text"],
            "date": row["review_date"]
        }

        for row in rows
    ]