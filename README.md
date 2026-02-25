# Django eCommerce Application

A web-based eCommerce platform built with Django and MariaDB. Users can register as vendors or buyers. Vendors can create stores and manage products, while buyers can browse stores, add products to their cart, checkout, and leave reviews.

## Features

- User registration and login as vendor or buyer
- Password reset via email with time-limited tokens
- Vendors can create, edit, and delete stores and products
- Buyers can add products to a session-based cart and checkout
- Invoice sent to buyer's email on checkout
- Verified and unverified product reviews
- Role-based access control using Django groups and permissions

## Requirements

- Python 3.x
- MariaDB

## Installation

1. Open a terminal and clone the repository, then navigate into the project folder:
    ```
    git clone https://github.com/AnnelienJanseVanRensburg/django-ecommerce
    cd your-repository-name
    ```

2. Create and activate a virtual environment:
    ```
    python -m venv venv
    venv\Scripts\activate
    ```

3. Install dependencies:
    ```
    pip install -r requirements.txt
    ```

4. Create a `.env` file in the root directory with the following:
    ```
    SECRET_KEY=your-secret-key
    DEBUG=True
    DB_NAME=ecommerce_db
    DB_USER=root
    DB_PASSWORD=your-db-password
    DB_HOST=localhost
    DB_PORT=3306
    EMAIL_HOST_USER=your-email@gmail.com
    EMAIL_HOST_PASSWORD=your-gmail-app-password
    ```

    Note: `EMAIL_HOST_PASSWORD` must be a Gmail App Password, not your regular Gmail
    password. To generate one:
    - Go to your Google Account settings
    - Go to Security and ensure 2-Step Verification is turned on
    - Search for App Passwords
    - Create a new App Password and name it "Django"
    - Copy the 16 character password into your `.env` file as `EMAIL_HOST_PASSWORD`

    If email credentials are not configured, the application will still process
    checkouts successfully and display a warning message instead of sending an email.

5. Create the database in MariaDB. Open a new terminal and log into the MariaDB client
   using the following command, then enter your root password when prompted:
    ```
    mysql -u root -p
    ```
    Once logged in, run the following SQL command to create the database:
    ```sql
    CREATE DATABASE ecommerce_db;
    ```
    Then exit the MariaDB client:
    ```sql
    EXIT;
    ```

6. Run migrations:
    ```
    python manage.py makemigrations
    python manage.py migrate
    ```

7. Create a superuser for the admin panel:
    ```
    python manage.py createsuperuser
    ```

8. Create the vendor and buyer groups:
    ```
    python manage.py shell
    ```
    ```python
    from django.contrib.auth.models import Group
    Group.objects.create(name='vendor')
    Group.objects.create(name='buyer')
    exit()
    ```

9. Run the development server:
    ```
    python manage.py runserver
    ```

10. Visit `http://localhost:8000` in your browser.

## Usage

- Register as a vendor to create stores and add products
- Register as a buyer to browse stores, add items to your cart, and checkout
- Access the admin panel at `http://localhost:8000/admin`

## Email Configuration

This application uses Gmail SMTP to send password reset links and order invoices.
If the email server is unavailable or credentials are incorrect, the application will
continue to function normally. Checkouts will still be processed and orders saved to
the database, but invoice emails will not be sent. A warning message will be displayed
to the user in this case.

## Project Structure

```
ecommerce_project/
├── accounts/        - Authentication app (register, login, password reset)
├── store/           - Shop app (stores, products, cart, checkout, reviews)
├── templates/       - HTML templates
├── static/          - CSS and static files
├── .env             - Environment variables (not included in version control)
├── requirements.txt - Project dependencies
└── manage.py
```
