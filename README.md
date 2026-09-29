# 🛒 Amazon Price Tracker

A Chrome extension and Python-based web scraping application that collects Amazon product information and displays it directly inside a browser popup.

The project combines **Python, Flask, BeautifulSoup, JavaScript, HTML/CSS, SQLite, and Chart.js** to create a lightweight Amazon product tracking system.

## ✨ Features

* 🔍 Scrape Amazon product information
* 💰 Extract current product prices
* 📊 Store price snapshots for price-history tracking
* 📈 Display price history using a line chart
* ⭐ Extract product ratings
* 💬 Collect publicly available customer review information
* 📦 Extract product availability
* 🖼️ Display product images
* 📤 Export product information as CSV
* 🧩 Use the project directly as a Chrome extension
* 🗄️ Store product and review data locally using SQLite
* 🔌 Flask REST API connects the Chrome extension with the Python scraper

## 🛠️ Technologies Used

### Frontend / Chrome Extension

* HTML5
* CSS3
* JavaScript
* Chrome Extension Manifest V3
* Chart.js

### Backend

* Python
* Flask
* Flask-CORS
* BeautifulSoup4
* Requests
* Pandas

### Database

* SQLite

## 📁 Project Structure

```text
Amazon Price Tracker/
│
├── backend/
│   │
│   ├── app.py
│   ├── scraper.py
│   ├── database.py
│   ├── requirements.txt
│   │
│   ├── database/
│   │   └── products.db
│   │
│   └── exports/
│
│
├── extension/
│   │
│   ├── manifest.json
│   ├── popup.html
│   ├── popup.css
│   ├── popup.js
│   ├── content.js
│   ├── chart.min.js
│   ├── package.json
│   └── package-lock.json
│
└── README.md
```

## 🔄 How It Works

```text
                Amazon Product Page
                         │
                         ▼
                   Chrome Extension
                         │
                         ▼
                     popup.js
                         │
                         │ HTTP Request
                         ▼
                  Flask REST API
                         │
                         ▼
                    scraper.py
                         │
                         ▼
                    Amazon HTML
                         │
                         ▼
                  BeautifulSoup
                         │
             ┌───────────┼───────────┐
             ▼           ▼           ▼
          Product      Price       Reviews
           Data        Data         Data
             │           │           │
             └───────────┼───────────┘
                         ▼
                     SQLite
                         │
                         ▼
                  Flask JSON API
                         │
                         ▼
                  Chrome Extension
                         │
              ┌──────────┼──────────┐
              ▼          ▼          ▼
           Product    Price       Reviews
            Info      Chart        List
```

## 🚀 Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/amazon-price-tracker.git
cd amazon-price-tracker
```

### 2. Create a Python virtual environment

```bash
python -m venv venv
```

### 3. Activate the virtual environment

#### Windows PowerShell

```powershell
.\venv\Scripts\Activate.ps1
```

#### Windows CMD

```cmd
venv\Scripts\activate.bat
```

### 4. Install Python dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 5. Start the Flask backend

```bash
python app.py
```

The API will run at:

```text
http://127.0.0.1:5000
```

You can test the server by opening the address in your browser.

## 🧩 Install the Chrome Extension

1. Open Chrome.
2. Navigate to:

```text
chrome://extensions/
```

3. Enable **Developer mode**.
4. Click **Load unpacked**.
5. Select the project's:

```text
extension/
```

folder.

Make sure `manifest.json` is directly inside the selected folder.

```text
extension/
├── manifest.json
├── popup.html
├── popup.css
├── popup.js
└── content.js
```

6. Pin **Amazon Price Tracker** to your Chrome toolbar.

## ▶️ Using the Extension

1. Start the Flask backend.
2. Open an Amazon product page.
3. Refresh the page.
4. Click the **Amazon Price Tracker** extension.
5. The extension sends the product URL to the Flask backend.
6. The backend extracts available product information.
7. Product information is stored in SQLite.
8. The extension displays the collected information.

## 📊 Price History

Every successful product scrape can create a price snapshot in the SQLite database.

The stored information includes:

```text
Product URL
Product Title
Price
Price Value
Date / Time
```

These snapshots can then be used to build a historical price chart.

For example:

```text
Price
 ₹3000 │        ●
       │       / \
 ₹2500 │  ●───/   ●
       │ /
 ₹2000 │●
       └────────────────
        Jan Feb Mar Apr
```

The accuracy and usefulness of the historical graph depend on how frequently the product is scraped and recorded.

## 💬 Reviews

The scraper attempts to collect publicly available review information such as:

* Reviewer name
* Rating
* Review title
* Review text
* Review date

The extension displays the collected reviews inside the popup.

## 📤 CSV Export

Product information can be exported as a CSV file.

Example:

```text
Product Name,Price,Rating,Reviews,Availability,URL
Example Product,₹2499,4.5,2341,In Stock,https://...
```

## 📦 NPM / Chart.js

The extension uses Chart.js for the price-history visualization.

Install the dependency with:

```bash
cd extension
npm install
```

The browser-compatible Chart.js build is included as:

```text
chart.min.js
```

## 🔐 Privacy

This project is designed as a local development project.

* Product data is stored locally in SQLite.
* The Flask API runs on the user's computer.
* No external database is required.
* No user account is required.
* The project does not require a third-party paid scraping API.

## ⚠️ Important Notes

This project is intended for **educational and personal development purposes**.

Amazon may change its website structure, HTML selectors, pricing layouts, or anti-bot mechanisms at any time. As a result, scraping results may vary between products, regions, and time periods.

The scraper should not be used to bypass CAPTCHA, authentication, access restrictions, or other security mechanisms.

Users should review and comply with the applicable website terms, policies, and laws when using the project.

## 🔮 Future Improvements

Planned improvements include:

* 🔔 Price-drop notifications
* ⏰ Automatic scheduled price checks
* 📉 Lowest-price detection
* 📈 7-day / 30-day / 6-month / 1-year price views
* 💾 Better product tracking
* 🏷️ Price-drop percentage calculation
* 📧 Email notifications
* 🔔 Chrome notifications
* 🛍️ Support for additional Amazon regions
* 🎨 Improved extension UI
* 📊 Product comparison
* 🔎 Search and manage tracked products
* 🧠 Better handling of different Amazon page layouts

## 📚 Project Purpose

This project was built to practice and demonstrate:

* Web scraping with Python
* HTML parsing with BeautifulSoup
* REST API development with Flask
* Chrome Extension development
* JavaScript browser APIs
* SQLite database management
* Data visualization with Chart.js
* CSV data export
* Frontend-backend communication

## 👨‍💻 Author

**Vigilant**

Built as a personal software development project to explore web scraping, browser extensions, APIs, databases, and data visualization.

````

### Suggested GitHub repository name

I'd use:

```text
amazon-price-tracker
````

And a short GitHub description:

> **A Chrome extension and Python/Flask application for tracking Amazon product prices, ratings, reviews, and price history.**

For your GitHub repo, I'd also add a proper **`.gitignore`** so you don't accidentally upload `venv`, `__pycache__`, `products.db`, or other generated files.
## 👨‍💻 Author

**Vigilant**

Built as a personal software development project to explore web scraping, browser extensions, APIs, databases, and data visualization.
