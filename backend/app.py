from flask import (
    Flask,
    jsonify,
    request,
    send_file
)

from flask_cors import CORS

import pandas as pd
import os

from scraper import scrape_product

from database import (
    initialize_database,
    save_product,
    save_reviews,
    get_price_history,
    get_reviews
)


app = Flask(__name__)

CORS(app)


EXPORT_FOLDER = "exports"

os.makedirs(
    EXPORT_FOLDER,
    exist_ok=True
)


initialize_database()


@app.route("/")
def home():

    return jsonify({

        "status": "online",

        "service":
            "Amazon Product Tracker API"

    })


@app.route(
    "/api/scrape",
    methods=["POST"]
)
def scrape():

    data = request.get_json()

    if not data:

        return jsonify({

            "error":
                "No JSON data received."

        }), 400


    url = data.get(
        "url",
        ""
    ).strip()


    if not url:

        return jsonify({

            "error":
                "Product URL is required."

        }), 400


    if "amazon." not in url.lower():

        return jsonify({

            "error":
                "Invalid Amazon URL."

        }), 400


    product = scrape_product(
        url
    )


    if "error" in product:

        return jsonify(
            product
        ), 500


    save_product(
        product
    )


    if product["review_data"]:

        save_reviews(

            product["url"],

            product["review_data"]

        )


    product["history"] = (
        get_price_history(
            product["url"]
        )
    )


    product["reviews_data"] = (
        get_reviews(
            product["url"]
        )
    )


    return jsonify(
        product
    )


@app.route(
    "/api/history",
    methods=["GET"]
)
def history():

    url = request.args.get(
        "url",
        ""
    )


    return jsonify(
        get_price_history(
            url
        )
    )


@app.route(
    "/api/reviews",
    methods=["GET"]
)
def reviews():

    url = request.args.get(
        "url",
        ""
    )


    return jsonify(
        get_reviews(
            url
        )
    )


@app.route(
    "/api/export",
    methods=["POST"]
)
def export():

    data = request.get_json()


    df = pd.DataFrame([{

        "Product Name":
            data.get("title"),

        "Price":
            data.get("price"),

        "Rating":
            data.get("rating"),

        "Reviews":
            data.get("reviews"),

        "Availability":
            data.get("availability"),

        "URL":
            data.get("url")

    }])


    filepath = os.path.join(
        EXPORT_FOLDER,
        "product_export.csv"
    )


    df.to_csv(
        filepath,
        index=False
    )


    return send_file(
        filepath,
        as_attachment=True
    )


if __name__ == "__main__":

    app.run(

        host="127.0.0.1",

        port=5000,

        debug=True

    )