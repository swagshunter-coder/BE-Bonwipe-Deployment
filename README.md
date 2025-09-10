# Bonewipe Backend (FastAPI)

Bonewipe Backend is a backend service designed for web development projects, providing robust APIs for authentication, product management, order processing, and more. Built with Python and FastAPI, it follows best practices for scalability, maintainability, and security.

## Features

- User authentication and authorization
- Product and category management
- Order processing
- Bank integration
- Modular and clean code structure
- Easy database setup

## Project Structure

```
BE-Bonewipe/
├── app/
│   ├── crud.py
│   ├── database.py
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   └── routes/
│       ├── auth.py
│       ├── banks.py
│       ├── categories.py
│       ├── orders.py
│       └── products.py
├── create_tables.py
├── requirements.txt
└── README.md
```

## Getting Started

### Prerequisites

- Python 3.10 or higher
- pip (Python package manager)
- Git

### Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/wildanmujjahid29/Bonewipe-Backend-FastAPI.git
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Set up the database:
   ```sh
   python create_tables.py
   ```
4. Run the application:
   ```sh
   python app/main.py
   ```

## API Endpoints

- `/auth` - Authentication routes
- `/products` - Product management
- `/categories` - Category management
- `/orders` - Order processing
- `/banks` - Bank-related operations
