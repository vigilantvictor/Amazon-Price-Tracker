import re
import requests

from bs4 import BeautifulSoup


# --------------------------------------------------
# AMAZON REQUEST SETTINGS
# --------------------------------------------------

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/142.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-IN,en;q=0.9",
    "Accept": (
        "text/html,application/xhtml+xml,"
        "application/xml;q=0.9,image/avif,"
        "image/webp,*/*;q=0.8"
    ),
    "DNT": "1",
    "Connection": "keep-alive"
}


# --------------------------------------------------
# PRICE CLEANING
# --------------------------------------------------

def extract_price_value(price_text):
    """
    Converts strings such as:

        ₹2,499
        ₹1,299.00
        2499
        Rs. 2,499

    into a float.
    """

    if not price_text:
        return None

    price_text = str(price_text).strip()

    if price_text == "N/A":
        return None

    # Remove commas
    cleaned = price_text.replace(",", "")

    # Find a number
    match = re.search(
        r"\d+(?:\.\d+)?",
        cleaned
    )

    if not match:
        return None

    try:
        return float(match.group())

    except ValueError:
        return None


# --------------------------------------------------
# FIND PRICE FROM HTML
# --------------------------------------------------

def find_price(soup):
    """
    Attempts several Amazon price selectors.
    """

    price_selectors = [

        # Current Amazon layouts
        "#corePriceDisplay_desktop_feature_div "
        ".a-price .a-offscreen",

        "#corePriceDisplay_mobile_feature_div "
        ".a-price .a-offscreen",

        "#corePriceDisplay_desktop_feature_div "
        ".a-price",

        "#corePrice_feature_div "
        ".a-price .a-offscreen",

        "#corePrice_feature_div "
        ".a-price",

        # Apex price section
        "#apex_desktop "
        ".a-price .a-offscreen",

        "#apex_desktop "
        ".a-price",

        # Older Amazon layouts
        "#priceblock_ourprice",

        "#priceblock_dealprice",

        "#priceblock_saleprice",

        # New price-to-pay layout
        ".priceToPay .a-offscreen",

        ".priceToPay",

        # Generic price
        ".a-price .a-offscreen",

        ".a-price"

    ]


    # ----------------------------------------------
    # Try CSS selectors
    # ----------------------------------------------

    for selector in price_selectors:

        try:

            element = soup.select_one(
                selector
            )

            if not element:
                continue

            text = element.get_text(
                " ",
                strip=True
            )

            if not text:
                continue

            value = extract_price_value(
                text
            )

            if value is not None:

                return {
                    "display": text,
                    "value": value
                }

        except Exception:

            continue


    # ----------------------------------------------
    # Try Amazon meta price
    # ----------------------------------------------

    meta_selectors = [

        'meta[itemprop="price"]',

        'meta[property="product:price:amount"]',

        'meta[name="price"]'

    ]


    for selector in meta_selectors:

        try:

            element = soup.select_one(
                selector
            )

            if not element:
                continue

            content = element.get(
                "content"
            )

            if not content:
                continue

            value = extract_price_value(
                content
            )

            if value is not None:

                return {
                    "display": f"₹{content}",
                    "value": value
                }

        except Exception:

            continue


    # ----------------------------------------------
    # Try JSON-LD product information
    # ----------------------------------------------

    scripts = soup.find_all(
        "script",
        type="application/ld+json"
    )


    for script in scripts:

        try:

            import json

            data = json.loads(
                script.string or script.get_text()
            )


            # Sometimes JSON-LD is a list
            if isinstance(
                data,
                list
            ):

                items = data

            else:

                items = [data]


            for item in items:

                if not isinstance(
                    item,
                    dict
                ):

                    continue


                offers = item.get(
                    "offers"
                )


                if not offers:
                    continue


                if isinstance(
                    offers,
                    list
                ):

                    offers = offers[0]


                if isinstance(
                    offers,
                    dict
                ):

                    json_price = offers.get(
                        "price"
                    )


                    if json_price:

                        value = extract_price_value(
                            json_price
                        )


                        if value is not None:

                            return {

                                "display":
                                    f"₹{json_price}",

                                "value":
                                    value

                            }


        except Exception:

            continue


    return {
        "display": "N/A",
        "value": None
    }


# --------------------------------------------------
# SCRAPE PRODUCT
# --------------------------------------------------

def scrape_product(url):

    try:

        # ------------------------------------------
        # Validate URL
        # ------------------------------------------

        if not url:

            return {
                "error":
                    "Product URL is empty."
            }


        if "amazon." not in url.lower():

            return {
                "error":
                    "The URL does not appear to be an Amazon URL."
            }


        # ------------------------------------------
        # Request Amazon
        # ------------------------------------------

        response = requests.get(

            url,

            headers=HEADERS,

            timeout=20,

            allow_redirects=True

        )


        response.raise_for_status()


        # ------------------------------------------
        # Parse HTML
        # ------------------------------------------

        soup = BeautifulSoup(

            response.text,

            "html.parser"

        )


        # ------------------------------------------
        # TITLE
        # ------------------------------------------

        title_element = soup.select_one(
            "#productTitle"
        )


        if title_element:

            title = title_element.get_text(
                " ",
                strip=True
            )

        else:

            title = "N/A"


        # ------------------------------------------
        # PRICE
        # ------------------------------------------

        price_data = find_price(
            soup
        )


        price = price_data[
            "display"
        ]


        price_value = price_data[
            "value"
        ]


        # ------------------------------------------
        # RATING
        # ------------------------------------------

        rating = "N/A"


        rating_selectors = [

            "span[data-hook='rating-out-of-text']",

            "#acrPopover",

            "i[data-hook='average-star-rating'] span"

        ]


        for selector in rating_selectors:

            element = soup.select_one(
                selector
            )


            if element:

                text = element.get_text(
                    " ",
                    strip=True
                )


                if not text:

                    text = element.get(
                        "title",
                        ""
                    )


                if text:

                    rating = text

                    break


        # ------------------------------------------
        # REVIEW COUNT
        # ------------------------------------------

        review_count = "N/A"


        review_count_selectors = [

            "span[data-hook='total-review-count']",

            "#acrCustomerReviewText"

        ]


        for selector in review_count_selectors:

            element = soup.select_one(
                selector
            )


            if element:

                text = element.get_text(
                    " ",
                    strip=True
                )


                if text:

                    review_count = text

                    break


        # ------------------------------------------
        # AVAILABILITY
        # ------------------------------------------

        availability = "N/A"


        availability_element = soup.select_one(
            "#availability span"
        )


        if availability_element:

            availability = (
                availability_element.get_text(
                    " ",
                    strip=True
                )
            )


        # ------------------------------------------
        # PRODUCT IMAGE
        # ------------------------------------------

        image = "N/A"


        image_selectors = [

            "#landingImage",

            "#imgBlkFront",

            "#ebooksImgBlkFront"

        ]


        for selector in image_selectors:

            image_element = soup.select_one(
                selector
            )


            if image_element:

                image = (

                    image_element.get(
                        "data-old-hires"
                    )

                    or image_element.get(
                        "src"
                    )

                    or "N/A"

                )

                if image != "N/A":

                    break


        # ------------------------------------------
        # REVIEWS
        # ------------------------------------------

        extracted_reviews = []


        review_elements = soup.select(
            "div[data-hook='review']"
        )


        for review in review_elements[:10]:

            # Reviewer
            reviewer_element = (
                review.select_one(
                    ".a-profile-name"
                )
            )


            reviewer = (

                reviewer_element.get_text(
                    " ",
                    strip=True
                )

                if reviewer_element

                else "Anonymous"

            )


            # Rating
            rating_element = (
                review.select_one(
                    "i[data-hook='review-star-rating'] span"
                )
            )


            review_rating = (

                rating_element.get_text(
                    " ",
                    strip=True
                )

                if rating_element

                else "N/A"

            )


            # Review title
            title_element = (
                review.select_one(
                    "a[data-hook='review-title']"
                )
            )


            review_title = (

                title_element.get_text(
                    " ",
                    strip=True
                )

                if title_element

                else ""

            )


            # Review text
            text_element = (
                review.select_one(
                    "span[data-hook='review-body']"
                )
            )


            review_text = (

                text_element.get_text(
                    " ",
                    strip=True
                )

                if text_element

                else ""

            )


            # Review date
            date_element = (
                review.select_one(
                    "span[data-hook='review-date']"
                )
            )


            review_date = (

                date_element.get_text(
                    " ",
                    strip=True
                )

                if date_element

                else "N/A"

            )


            extracted_reviews.append({

                "reviewer":
                    reviewer,

                "rating":
                    review_rating,

                "title":
                    review_title,

                "text":
                    review_text,

                "date":
                    review_date

            })


        # ------------------------------------------
        # RETURN PRODUCT
        # ------------------------------------------

        return {

            "url":
                url,

            "title":
                title,

            "price":
                price,

            "price_value":
                price_value,

            "rating":
                rating,

            "reviews":
                review_count,

            "availability":
                availability,

            "image":
                image,

            "review_data":
                extracted_reviews

        }


    except requests.exceptions.Timeout:

        return {

            "error":
                "Amazon request timed out."

        }


    except requests.exceptions.HTTPError as error:

        return {

            "error":
                f"Amazon returned HTTP error: {error}"

        }


    except requests.exceptions.RequestException as error:

        return {

            "error":
                f"Network error: {error}"

        }


    except Exception as error:

        return {

            "error":
                f"Scraper error: {error}"

        }