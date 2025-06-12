# E-commerce Backend System (FastAPI)

This is the backend REST API for an E-commerce platform, built using FastAPI. It supports user authentication, product management, shopping cart operations, order placement, password reset via email, and refresh token-based session management.

---

## Features

### Authentication & Authorization
- User registration & login with JWT (Access + Refresh tokens)
- Role-based access control (`admin`, `user`)
- Secure password hashing with bcrypt
- Forgot & Reset password via email (SMTP)

### Product Management
- Admin-only Create, Update, Delete products
- Public product browsing
- Optional image URLs for product display

### Cart & Checkout
- View, add, update, delete items from cart
- Dummy checkout endpoint, create order

### Order
- View order history & Order details

### Refresh Token Handling
- Persistent login with refresh tokens
- Secure token rotation & expiry


---

## Tech Stack

Framework: FastAPI                   
Language:  Python 3.12                     
ORM: SQLAlchemy                      
Database: PostgreSQL / SQLite (dev)       
Auth: JWT via `python-jose`           
Password Hash: `passlib` with `bcrypt`         
Email Service: SMTP using `smtplib`            
Env Config: `python-dotenv` 
Version Control: GitHub                

---

## Project Structure

```
ecommerce_backend/
├── alembic
├── app/
│ ├── auth/ # Authentication logic,email utils
│ ├── products/ # Product endpoints/models
│ ├── cart/ # Cart endpoints
│ ├── orders/ # order endpoints 
│ ├── checkout/ # Checkout logic
│ ├── core/ # DB, config, 
│ ├── middleware/ # logging, JWT auth
│ ├── utils/ # Checkout logic
│ └── main.py # App entry point
├── logs/
│ └── log_file.py # handle logs   
├── venv
├── .env # Environment variables
├── alembic.ini
└── ecommerce.db
├── README.md
├── requirements.txt
├── seed_data.py # Sample product seeding

```
---

### Prerequisites

- Python 3.12.10
- Postman
- SQLiteStudio
- SMTP Email credentials (Gmail, Mailtrap, etc.)
- Vscode Editor

---

##  Installation & Setup

Follow these steps to set up the project locally:

### 1. Clone the Repository

```bash
git https://github.com/Pakhi-21/E-Commerce_Backend.git
```

### 2. Navigate to the Project Directory

```bash
cd ecommerce_backend
```

### 3. Create a virtual Environment

```bash
python3 -m venv venv
```

### 4. Activate the Virtual Environment On Windows:

```bash
venv\Scripts\activate
```
### 5. Install Dependencies

```bash
pip install -r requirements.txt
```
### 6. Run the Application

```bash
uvicorn app.main:app --reload
```
### The API will be accessible at http://127.0.0.1:8000/

### Access the Swagger UI at http://127.0.0.1:8000/docs/

---
## API Endpoints

- **Authentication:** `http://127.0.0.1:8000/auth`
- **Products Management:** `http://127.0.0.1:8000/admin/products`
- **Cart Management:** `http://127.0.0.1:8000/cart`
- **Checkout Management:** `http://127.0.0.1:8000/checkout`
- **Order Management:** `http://127.0.0.1:8000/order`

---

## Future Enchancement

- Secure Payment Gateway Integration (e.g., Razorpay, PayPal)

- Implement Recommendation System using ML to suggest products

- Admin Dashboard with Analytics  

---

## License

### This project is open-source under the [MIT License].

---









