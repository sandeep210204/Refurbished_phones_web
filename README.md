# 📱 Refurbished Phones Inventory Management (Flask App)

A simple yet functional **inventory management system** for refurbished phones, built using **Flask** and **SQLite**.
This project was developed as part of a technical assignment and demonstrates **CRUD operations, authentication, bulk uploads, and platform-based listings**.

---

## 🚀 Features

* 🔑 **Login / Logout** (mock authentication with session handling)
* 📦 **Add / Edit / Delete Phones** in the inventory
* 📊 **Search & Filter** phones by model, brand, condition, or listing platform
* 🏷️ **B2B Reservations** – reserve stock specifically for bulk buyers
* 💲 **Auto Price Calculation** for 3 platforms (X, Y, Z) with different fee structures
* ✅ **Profitability Check** – ensures at least \$5 profit before listing on any platform
* 📤 **Bulk Upload (CSV/Excel)** to quickly add multiple phones
* 🏷️ **Tags** (e.g., “Out of Stock”) to highlight inventory status

---

## 🛠️ Tech Stack

* **Backend**: Flask (Python)
* **Database**: SQLite (via SQLAlchemy ORM)
* **Frontend**: Jinja2 Templates (HTML + Bootstrap for styling)
* **File Uploads**: Pandas + OpenPyXL for CSV/Excel handling
* **Containerization**: Docker-ready

---

## 📂 Project Structure

```
Task/
│── app.py                # Main Flask application
│── requirements.txt       # Dependencies
│── storage.db             # SQLite database (auto-created)
│── uploads/               # Uploaded CSV/Excel files
│── templates/             # HTML templates
│   ├── layout.html
│   ├── index.html
│   ├── add_phone.html
│   ├── edit_phone.html
│   ├── login.html
│   └── upload.html
│── static/
    └── css/style.css      # Custom styles
```

---

## ⚙️ Installation & Setup

### 🔹 Option 1: Run Locally

1. Clone this repository

   ```bash
   git clone https://github.com/sandeep210204/Refurbished_phones_web.git
   cd Refurbished_phones_web
   ```
2. Create virtual environment & install dependencies

   ```bash
   pip install -r requirements.txt
   ```
3. Run the Flask app

   ```bash
   python app.py
   ```
4. Open in browser: **[http://127.0.0.1:5000/](http://127.0.0.1:5000/)**

👉 Login credentials:

* **Username**: `admin`
* **Password**: `password123`

---

### 🔹 Option 2: Run with Docker

1. Build the image

   ```bash
   docker build -t refurbished-phones-app .
   ```
2. Run the container

   ```bash
   docker run -p 5000:5000 refurbished-phones-app
   ```
3. Open in browser: **[http://localhost:5000](http://localhost:5000)**

---

## 📤 Bulk Upload Example

Upload a **CSV/Excel** file with the following columns:

| model\_name | brand   | base\_price | stock\_quantity | condition | specifications | reserved\_for\_b2b |
| ----------- | ------- | ----------- | --------------- | --------- | -------------- | ------------------ |
| Galaxy S10  | Samsung | 200         | 10              | Good      | 128GB, Black   | 2                  |
| iPhone 11   | Apple   | 350         | 5               | New       | 64GB, White    | 0                  |

---

## 🎥 Video Explanation

📌 [Link to Video Walkthrough](#) *(Add your Loom/YouTube/Drive link here)*

The video covers:

1. Project overview
2. Code walkthrough
3. Demo of features (login, add/edit/delete, upload, listing)
4. Running via Docker

---

## 📌 Notes for Recruiter

* ✅ This project demonstrates **Flask fundamentals, SQLAlchemy ORM, authentication, CRUD, file handling, and Docker**.
* ✅ The code is **beginner-friendly**, easy to explain in an interview.
* ✅ Both repository and video are shared as per requirements.

---

## 👨‍💻 Author

**Vandrangi Sandeep**
📧 Email: *\[sandeepvandrangi@gmail.com]*
🔗 GitHub: [sandeep210204](https://github.com/sandeep210204)

---

Would you like me to also prepare a **script/outline for your video explanation** (so you can record confidently and hit all the points the recruiter expects)?
