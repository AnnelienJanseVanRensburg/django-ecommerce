# Django eCommerce Application

A web-based eCommerce platform built with Django and MariaDB. Users can register as vendors or buyers. Vendors can create stores and manage products, while buyers can browse stores, add products to their cart, checkout, and leave reviews.
Includes a RESTful API built with Django REST Framework.

## Features

- User registration and login (vendor or buyer roles)
- Password reset via email with time-limited tokens
- Vendors can create, edit, and delete stores and products
- Buyers can add products to a session-based cart and checkout
- Invoice sent to buyer's email on checkout
- Verified and unverified product reviews
- Role-based access control using Django groups and permissions

## Requirements

- Python 3.x
- MariaDB
- A Gmail account with an App Password for email functionality

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
    Note: User groups (vendor and buyer) and their permissions are created
    automatically when migrations are run.

7. Create a superuser for the admin panel:
    ```
    python manage.py createsuperuser
    ```

8. Run the development server:
    ```
    python manage.py runserver
    ```

9. Visit `http://localhost:8000` in your browser.

## Usage

- Register as a vendor to create stores and add products
- Register as a buyer to browse stores, add items to your cart, checkout, and leave reviews 
- Access the admin panel at `http://localhost:8000/admin`

## Email Configuration

This application uses Gmail SMTP to send password reset links and order invoices.
If the email server is unavailable or credentials are incorrect, the application will
continue to function normally. Checkouts will still be processed and orders saved to
the database, but invoice emails will not be sent. A warning message will be displayed
to the user in this case.

For security reasons, the password reset page does not confirm whether an email
address is registered in the system.

## Project Structure

```
eCommerce-Web-App/
├── accounts/           - Authentication app (register, login, password reset)
├── ecommerce_project/  - Main files
├── store/              - Shop app (stores, products, cart, checkout, reviews)
├── templates/          - HTML templates
├── static/             - CSS and static files
├── .env                - Environment variables (not included in version control)
├── requirements.txt    - Project dependencies
└── manage.py
```
