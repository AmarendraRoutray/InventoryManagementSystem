
# Inventory Management System

This project is a backend API for managing inventory items using Django Rest Framework. It includes authentication via JWT, caching with Redis, PostgreSQL as the database, and logging for debugging and monitoring. The system supports CRUD operations and is built with performance, security, and testing in mind.

## Features

- **CRUD Operations**: Create, Read, Update, Delete inventory items.
- **Authentication**: Secure access to the API using JWT authentication.
- **Caching**: Redis caching for improving performance.
- **Database**: PostgreSQL for storing inventory data.
- **Logging**: Logs for API usage, errors, and monitoring.
- **Unit Testing**: Comprehensive tests for all endpoints.

## Prerequisites

- Python 3.8+
- PostgreSQL
- Redis
- Django
- pgAdmin (for managing the PostgreSQL database)

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <repository-url>
cd Inventory-Management-System
```

### 2. Create a Virtual Environment

It's recommended to use a virtual environment to isolate your project dependencies:

```bash
python -m venv venv
```

Activate the virtual environment:

- On Windows:
  ```bash
  venv\Scripts\activate
  ```
- On macOS/Linux:
  ```bash
  source venv/bin/activate
  ```

### 3. Install Required Packages

Install the dependencies from `requirements.txt`:

```bash
pip install -r requirements.txt
```

### 4. PostgreSQL Setup

You'll need to set up a PostgreSQL database for the project. Follow these steps:

#### Using pgAdmin:

1. Open **pgAdmin** and log in with your credentials.
2. Right-click on **Servers** and click **Create** -> **Server...**.
3. Name your server (e.g., `InventoryServer`) and go to the **Connection** tab.
4. Enter your PostgreSQL host, username, and password.
5. Click **Save**.
6. Now, right-click on your server name and select **Create** -> **Database...**.
7. Name your database (e.g., `inventory_db`) and click **Save**.
8. Make sure to update your `settings.py` file with your PostgreSQL database details.

### 5. Database Migrations

Once your PostgreSQL database is set up, run the following commands to apply migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create a Superuser

To create an admin user for the Django admin panel, run:

```bash
python manage.py createsuperuser
```

Follow the prompts to set the email, username, and password.

### 7. Run the Application

You can now run the development server:

```bash
python manage.py runserver
```

Your application will be accessible at `http://127.0.0.1:8000/`.

### 8. Thunder Client API Collection

We have included a Thunder Client API collection to make it easier to test the API endpoints.

#### Importing Thunder Client API Collection:

1. In **Visual Studio Code**, open the **Thunder Client** extension.
2. Click on the **Collections** tab.
3. Click the **Import** button.
4. Select the provided `thunder-client-collection.json` file from the project folder.
5. The API collection will be imported, and you can use it to test the different endpoints.

### 9. Redis Setup

Ensure that Redis is installed and running on your machine. To install Redis:

- On **Ubuntu**:
  ```bash
  sudo apt-get install redis-server
  ```

- On **macOS** (using Homebrew):
  ```bash
  brew install redis
  ```

Run Redis:

```bash
redis-server
```

Ensure that Redis is running on `127.0.0.1:6379` as per the configuration in your `settings.py`.

### 10. Run Tests

To run the unit tests for the API, use the following command:

```bash
python manage.py test
```

## API Documentation

After running the server, you can access the API documentation and explore the available endpoints using Thunder Client or directly through the Django Admin panel (if `drf-yasg` or `drf-spectacular` is used for API documentation).

## Contribution

Feel free to contribute by creating issues or sending pull requests.

## License

This project is licensed under the MIT License.
