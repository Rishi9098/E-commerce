# ShopHub — Django E-Commerce Platform

A full-stack e-commerce web application built with Django 6, supporting both **Buyers** and **Sellers** with role-based access control.

---

## Features

- **Buyer** — Browse products, add to cart, place orders, view order history
- **Seller** — Register as a seller, add/edit/delete products, manage listings via dashboard
- **Guest** — Browse products and add to cart (cart merges on login)
- HTMX-powered cart updates (no page reload)
- SweetAlert2 popups for cart actions and confirmations
- Bootstrap 5 responsive UI

---

## Tech Stack

| Layer       | Technology               |
|-------------|--------------------------|
| Backend     | Django 6.0.3             |
| Database    | SQLite (dev)             |
| Frontend    | Bootstrap 5, HTMX 1.9   |
| Auth        | Custom User Model        |
| Images      | Pillow                   |
| Alerts      | SweetAlert2              |

---

## Project Structure

```
ecommerce/
├── accounts/        # Custom user model, login, signup, logout
├── cart/            # Session & DB cart logic, HTMX cart views
├── orders/          # Order placement and order history
├── products/        # Product listings, seller dashboard
├── templates/       # All HTML templates
├── static/          # CSS and static assets
├── media/           # Uploaded product images
└── ecommerce/       # Project settings and URLs
```

---

## Installation & Setup

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd ecommerce
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv

# macOS/Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Apply migrations

```bash
python manage.py migrate
```

### 5. Create a superuser (admin)

```bash
python manage.py createsuperuser
```

### 6. Run the development server

```bash
python manage.py runserver
```

Visit: [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## User Roles

| Role   | Permissions                                              |
|--------|----------------------------------------------------------|
| Buyer  | Browse products, manage cart, place orders, view history |
| Seller | Add/edit/delete own products, view seller dashboard      |
| Admin  | Full access via `/admin/`                                |

---

## Key URLs

| URL                        | Description              |
|----------------------------|--------------------------|
| `/`                        | Product listing page     |
| `/accounts/signup/`        | Register as buyer/seller |
| `/accounts/login/`         | Login                    |
| `/accounts/logout/`        | Logout                   |
| `/cart/`                   | View cart                |
| `/orders/history/`         | Order history (buyers)   |
| `/seller/dashboard/`       | Seller dashboard         |
| `/admin/`                  | Django admin panel       |

---

## Environment Notes

- `DEBUG = True` — for development only, set to `False` in production
- `SECRET_KEY` — replace with a secure key before deploying
- `MEDIA_ROOT` — product images are stored in the `media/` folder
- Default database is **SQLite** — switch to PostgreSQL for production

---

## Screenshots

> Add screenshots of your product listing, cart, and dashboard pages here.

---

## License

This project is for educational/internship purposes.
