# Saudi Coffee Shop Guide ☕

A Python desktop application for managing coffee shops across Saudi Arabia. The application allows users to add, view, update, delete, search, and filter coffee shops, view statistics, and generate reports.

## Features

- **Coffee Shop Management:** Add, view, edit, and delete coffee shops.
- **Search:** Search coffee shops by name.
- **Filtering:** Filter records by city and category.
- **Statistics Dashboard:** View total coffee shops, average rating, highest-rated shop, and shops by city.
- **Report Generation:** Generate a text report containing coffee shop records and statistics.
- **Threading:** Generate reports using a background thread.
- **Data Persistence:** Store coffee shop information in an SQLite database.
- **Error Handling:** Handle invalid inputs, HTTP errors, connection failures, and timeouts.

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| Tkinter | Desktop graphical interface |
| Flask | Backend REST API |
| SQLite | Database management |
| urllib | HTTP communication between frontend and backend |
| threading | Background report generation |
| JSON | Data exchange between frontend and backend |

## Project Architecture

The application follows a client-server architecture:

```text
        User
         |
         v
   Tkinter GUI
         |
    HTTP Requests
         |
         v
    Flask Backend
         |
    DatabaseManager
         |
         v
    SQLite Database

    Report Generation
         |
    Background Thread
         |
         v
    Text Report File
```

Tkinter communicates with Flask through HTTP requests. Flask handles the requests and interacts with SQLite through the `DatabaseManager` class.

## Project Structure

```text
SaudiCoffeeGuide/
│
├── database/
│   └── coffee_shops.db
│
├── reports/
│   └── coffee_report.txt
│
├── app.py
├── gui.py
├── database.py
├── report.py
│
├── test_api.py
├── test_connection.py
│
├── requirements.txt
└── README.md
```

**Note:** The database and report files are generated automatically when needed.

## Installation and Setup

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

### 2. Navigate to the project directory

```bash
cd SaudiCoffeeGuide
```

### 3. Create a virtual environment

```bash
python -m venv .venv
```

### 4. Activate the virtual environment

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

## Running the Application

The application requires the Flask backend and Tkinter frontend to run separately.

### Terminal 1 – Start the Flask backend

```bash
python app.py
```

The server runs at:

```text
http://127.0.0.1:5050
```

### Terminal 2 – Start the Tkinter application

```bash
python gui.py
```

The desktop application will open and retrieve coffee shop records from the Flask backend.

## Database Design

The application uses SQLite with a table named `coffee_shops`.

| Column | Data Type | Description |
|---|---|---|
| id | INTEGER | Unique coffee shop ID |
| name | TEXT | Coffee shop name |
| city | TEXT | City location |
| rating | REAL | Rating between 0 and 5 |
| category | TEXT | Coffee shop category |
| notes | TEXT | Additional information |

The database uses an automatically generated primary key.

## API Endpoints

The Flask backend provides the following endpoints:

| HTTP Method | Endpoint | Description |
|---|---|---|
| GET | `/shops` | Retrieve all coffee shops |
| GET | `/shops/<shop_id>` | Retrieve one coffee shop |
| POST | `/shops/add` | Add a coffee shop |
| POST | `/shops/update/<shop_id>` | Update a coffee shop |
| POST | `/shops/delete/<shop_id>` | Delete a coffee shop |

The backend returns JSON responses with appropriate HTTP status codes.

## Python Course Concepts

The project demonstrates the following Python concepts:

| Course Concept | Implementation | Location |
|---|---|---|
| Variables and Data Types | Store coffee shop information | All Python files |
| Functions | Organize application operations | All Python files |
| Conditions | Validate inputs and handle errors | `app.py`, `gui.py` |
| Loops | Display records and calculate statistics | `gui.py`, `report.py` |
| Lists | Store retrieved coffee shop records | `gui.py`, `report.py` |
| Dictionaries | Handle records and count shops by city | `database.py`, `report.py` |
| Classes and Objects | Database and GUI classes | `database.py`, `gui.py` |
| Exception Handling | Handle database, HTTP, and connection errors | `app.py`, `gui.py` |
| File Handling | Generate text reports | `report.py` |
| SQLite | Store and retrieve coffee shop records | `database.py` |
| Threading | Generate reports in a background thread | `gui.py` |
| Flask | Implement backend API routes | `app.py` |
| JSON | Exchange data between frontend and backend | `app.py`, `gui.py` |

## Report Generation

The application generates a text report containing:

- Total number of coffee shops.
- Average rating.
- Highest-rated coffee shop.
- Number of coffee shops in each city.
- Complete coffee shop records.

The report is saved automatically in:

```text
reports/coffee_report.txt
```

Report generation runs in a separate thread to keep the Tkinter interface responsive.

## Testing

The project includes scripts for testing the backend and connection handling.

Run the Flask backend first.

Test API operations:

```bash
python test_api.py
```

Test server connectivity:

```bash
python test_connection.py
```

The application should also be tested through the Tkinter interface for CRUD operations, search, filtering, statistics, and report generation.

## Authors

- Student Name: [Mazen Hassan Bafaqih]
- Student ID: [443043723]
- Course: Python Programming

## License

This project was developed as an academic course project.
