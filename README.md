# 📱 Refurbished Phones Inventory Web Application

### 🔗 GitHub Repository

👉 [Refurbished\_phones\_web](https://github.com/sandeep210204/Refurbished_phones_web)

### 🎥 Video Explanation

👉 [Click here to watch the demo video](#) *(Replace `#` with your video link when ready)*

---

## 🚀 Project Overview

This project is a **Flask-based web application** built to manage and sell refurbished phones across **three simulated e-commerce platforms (X, Y, Z)**.

The system is designed as per the given assignment requirements:

* Handle **inventory management** (Add, Update, Delete, Bulk Upload).
* Apply **platform-specific pricing rules and fees**.
* Ensure **profitability checks** and **stock validation** before listing.
* Provide **search, filters, and bulk upload support** for easy management.
* Include **mock authentication** for basic security.

This is a **dummy application** with **no real platform integrations**, but it simulates how phones would be listed on each platform.

---

## 📋 Problem Statement (from Assignment)

* Build an application to manage and sell refurbished phones on three e-commerce platforms (**X, Y, Z**).
* Handle inventory, pricing, and platform-specific condition mapping.
* Prevent listing if:

  1. Phone is **out of stock** (reserved for B2B or zero stock).
  2. Fees make the sale **unprofitable**.
  3. Condition does not match platform requirements.

---

## 🛠️ Features Implemented

### 1. 📦 Phone Inventory Management

* Add, Update, Delete phones.
* Manage stock quantity and B2B reservations.
* Bulk upload via **CSV/Excel files**.
* Auto-calculate and store **platform-specific prices**.
* Show **tags** (like *Out of Stock*).

### 2. 💰 Platform-Specific Logic (Dummy Integration)

* **Price Calculation Rules**:

  * X → 10% fee
  * Y → 8% fee + \$2 fixed
  * Z → 12% fee
* **Condition Mapping**:

  * X → New, Good, Scrap
  * Y → Excellent (3★), Good (2★), Usable (1★)
  * Z → New, As New, Good
* Prevents unprofitable listings (< \$5 profit).

### 3. 🔍 Search and Filters

* Search phones by **Model Name** or **Brand**.
* Filter by **Condition** (New, Good, Scrap, etc.).
* Filter by **Platform Listing Status** (X, Y, Z).

### 4. 📤 Bulk Upload Support

* Upload phones using **CSV or Excel files**.
* Automatically processes multiple phones at once.
* Handles validation for incorrect rows.

### 5. 🔐 Security and Authentication

* **Mock login system** (username & password).
* **Input validation** and sanitization.

---

## 🏗️ Tech Stack

* **Backend**: Python (Flask)
* **Database**: SQLite (via SQLAlchemy)
* **Frontend**: HTML + Bootstrap (templates)
* **Libraries**:

  * `Flask`, `Flask-SQLAlchemy`, `Werkzeug`
  * `Pandas`, `OpenPyXL` (for Excel/CSV processing)

---

## 📂 Project Structure

```
Refurbished_phones_web/
│── app.py                 # Main Flask application  
│── requirements.txt       # Dependencies  
│── Dockerfile             # Docker build config  
│── instance/              # SQLite DB storage  
│── static/css/            # Custom CSS  
│── templates/             # HTML templates (Jinja2)  
│── uploads/               # Uploaded CSV/Excel files  
│── README.md              # Documentation (this file)  
```

---

## ▶️ How to Run Locally

### **Option 1: Run Normally**

```bash
# Clone the repo
git clone https://github.com/sandeep210204/Refurbished_phones_web.git
cd Refurbished_phones_web

# Install dependencies
pip install -r requirements.txt

# Run the app
python app.py
```

App runs at 👉 **[http://127.0.0.1:5000/](http://127.0.0.1:5000/)**

### **Option 2: Run with Docker**

```bash
# Build the image
docker build -t refurbished-phones-app .

# Run the container
docker run -p 5000:5000 refurbished-phones-app
```

---

## ✅ Assignment Criteria Checklist

✔️ **Problem Solving (30%)** → Inventory, pricing, conditions, profitability implemented.
✔️ **Code Quality (30%)** → Modular, validated, documented.
✔️ **Security (20%)** → Mock authentication, input sanitization.
✔️ **Functionality (20%)** → End-to-end demo with all features.
⭐ **Bonus (5%)** → Implemented using **Python (Flask backend)**.

---

## 📌 Next Steps

* [ ] Deploy on DockerHub/Heroku for bonus visibility (optional).

---

⚡ Developed by **Sandeep Vandrangi** as part of the **Refurbished Phone Selling Assignment**.

---
