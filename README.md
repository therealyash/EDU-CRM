# EDU-CRM

A robust Customer Relationship Management (CRM) system developed using Django.

## Features
- Efficient management of customer data
- User-friendly interface for handling CRM operations
- Customizable to suit various business needs

## Prerequisites
Ensure you have the following installed before proceeding:
- Python 3.8+
- pip (Python package installer)

## Setup Guide
Follow these steps to set up and run the CRM project locally:

### 1. Create a Virtual Environment
Create and activate a virtual environment to isolate dependencies.
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

### 2. Install Dependencies
Install all required packages listed in `requirements.txt`.
```bash
pip install -r requirements.txt
```

### 3. Apply Migrations
Run database migrations to set up the database schema.
```bash
python manage.py migrate
```

### 4. Create a Superuser
Set up an administrative user to access the Django admin panel.
```bash
python manage.py createsuperuser
```

### 5. Start the Development Server
Launch the Django development server.
```bash
python manage.py runserver
```

Visit the application at [http://127.0.0.1:8000/](http://127.0.0.1:8000/).

## Contributing
Contributions are welcome! If you’d like to contribute, please fork the repository and submit a pull request with your changes.

## License
This project is licensed under the MIT License. See the `LICENSE` file for more details.
