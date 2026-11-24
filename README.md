# My Coffee Journal ☕

**My Coffee Journal** is a Python desktop application for keeping a
personal record of coffee shops across Saudi Arabia. It lets users
discover and organize their coffee shop entries, add ratings and notes,
search and filter saved places, view statistics, and generate a report.

**GitHub repository:** https://github.com/Mazzz10/MyCoffeeJournal

## Features


- **Coffee shop management:** Add, view, edit, and delete coffee shop
    records.
- **Instant search:** Search records by coffee shop name as the user
    types.
- **Filtering:** Filter records by city and category.
- **Statistics dashboard:** View the total number of shops, average
    rating, highest-rated shop, and number of shops by city.
- **Report generation:** Generate a UTF-8 text report containing
    summary statistics and all saved records.
- **Background processing:** Generate reports in a daemon worker
    thread while the Tkinter interface remains responsive.
- **Persistent storage:** Store records in an SQLite database.
- **Validation and error handling:** Validate required fields and
    ratings; handle HTTP errors, unavailable servers, and connection
    timeouts.

## Technologies

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| Tkinter / ttk | Desktop graphical user interface |
| Flask | Backend HTTP API |
| SQLite | Persistent database |
| `urllib.request` | Send HTTP requests from the GUI and test scripts |
| `urllib.parse` | Encode POST form data |
| `json` | Decode JSON responses |
| `threading` | Run report generation in a background thread |
| `queue` | Pass worker results safely to the Tkinter thread |
| `pathlib` | Build database and report paths |

## Architecture

The application uses a client-server architecture:

``` text
User
 |
 v
Tkinter GUI (gui.py)
 |
 | HTTP GET / POST requests
 v
Flask API (app.py)
 |
 v
DatabaseManager (database.py)
 |
 v
SQLite (database/coffee_shops.db)


Report workflow:
Tkinter Generate Report button
 |
 v
Worker thread (gui.py)
 |                         \
 | GET /shops                \ generate_report(shops)
 v                             v
Flask API                    report.py
                               |
                               v
                     reports/coffee_report.txt
```

The Tkinter interface sends HTTP requests to Flask. Flask validates
submitted values and calls `DatabaseManager` for database operations.
The GUI does not connect directly to SQLite.

## Project Structure

``` text
MyCoffeeJournal/
├── database/
│   └── coffee_shops.db       # SQLite database (created/used at runtime)
├── reports/
│   └── coffee_report.txt     # Generated when a report is created
├── app.py                    # Flask routes and backend validation
├── database.py               # DatabaseManager and SQLite operations
├── gui.py                    # Tkinter application and HTTP client
├── report.py                 # Text report generation
├── test_api.py               # API CRUD and validation test script
├── test_connection.py        # Basic Flask connectivity test
├── requirements.txt          # Flask and its pinned dependencies
├── .gitignore
└── README.md
```

The `database` and `reports` directories/files are created as needed.
The application initializes the database table automatically when the
Flask backend starts. A generated report is not required to run the
application.

## Installation and Setup

### 1. Clone the repository

``` bash
git clone https://github.com/Mazzz10/MyCoffeeJournal.git MyCoffeeJournal
cd MyCoffeeJournal
```

### 2. Create a virtual environment

``` bash
python -m venv .venv
```

### 3. Activate the virtual environment

**Windows PowerShell:**

``` powershell
.venv\Scripts\Activate.ps1
```

**Windows Command Prompt:**

``` bat
.venv\Scripts\activate.bat
```

**macOS / Linux:**

``` bash
source .venv/bin/activate
```

### 4. Install dependencies

``` bash
python -m pip install -r requirements.txt
```

`requirements.txt` contains Flask and its pinned dependencies. Modules
such as `sqlite3`, `tkinter`, `threading`, `queue`, `json`, `pathlib`,
and `urllib` are part of Python's standard library. Tkinter must also be
available in the local Python installation.

## Running the Application

Run the Flask backend and Tkinter frontend in two separate terminals.
Activate the virtual environment in both terminals.

### Terminal 1 --- Start Flask

``` bash
python app.py
```

The backend listens on:

``` text
http://127.0.0.1:5050
```

Keep this terminal running.

### Terminal 2 --- Start Tkinter

``` bash
python gui.py
```

The My Coffee Journal window opens and requests the saved records
from Flask. During normal use, users interact with the Tkinter window
and do not need to send HTTP requests manually.

## Database Initialization and Design

The database is initialized automatically when `app.py` creates the
`DatabaseManager` object.

`DatabaseManager.__init__()` in `database.py`:

1.  Sets the database path to `database/coffee_shops.db`.
2.  Creates the `database` directory if it does not exist.
3.  Calls `create_table()`.

`create_table()` uses `CREATE TABLE IF NOT EXISTS`. It creates the table
if it is missing and does not drop existing records when the application
starts. No manual SQL command is required.

### Table: `coffee_shops`

| Column | SQLite type | Purpose |
|---|---|---|
| `id` | `INTEGER PRIMARY KEY AUTOINCREMENT` | Unique record identifier |
| `name` | `TEXT NOT NULL` | Coffee shop name |
| `city` | `TEXT NOT NULL` | City |
| `rating` | `REAL NOT NULL` | Rating from 0 to 5 |
| `category` | `TEXT NOT NULL` | Coffee shop category |
| `notes` | `TEXT` | Optional notes |

Each database operation opens its own SQLite connection and closes it in
a `finally` block. Operations that change data call `commit()`. SQL
values are passed using `?` placeholders.

## API Endpoints

The Flask backend in `app.py` provides these routes:

| HTTP method | Endpoint | Purpose | Success status |
|---|---|---|---:|
| GET | `/shops` | Retrieve all coffee shops | 200 |
| GET | `/shops/<shop_id>` | Retrieve one coffee shop by ID | 200 |
| POST | `/shops/add` | Add a coffee shop | 201 |
| POST | `/shops/update/<shop_id>` | Update a coffee shop | 200 |
| POST | `/shops/delete/<shop_id>` | Delete a coffee shop | 200 |

The API returns JSON responses. Missing required values, non-numeric
ratings, and ratings outside 0--5 return HTTP 400. A request for a
record that does not exist returns HTTP 404. Unexpected backend errors
return HTTP 500.

The GUI uses `urlopen()` to send requests, `urlencode()` to encode POST
form data, and `json.loads()` to decode JSON responses. The GUI handles
HTTP errors, URL/connection errors, and socket timeouts.

## Python Course Topics and Implementation Locations

The following table identifies where the course topics appear in the
submitted source files.

| Course topic | Implementation evidence | File and relevant location |
|---|---|---|
| Python, variables, and data types | Form values, records, IDs, ratings, and status values | Throughout `app.py`, `database.py`, `gui.py`, and `report.py` |
| Functions | Reusable operations and route handlers | Flask routes in `app.py`; methods in `DatabaseManager` and `CoffeeShopApp`; `generate_report()` in `report.py` |
| Conditions | Validate fields and ratings, handle missing records, and filter records | `add_shop()` and `update_shop()` in `app.py`; `save_shop()`, `apply_filters()`, and `delete_shop()` in `gui.py` |
| Loops | Process records, populate the table, and generate reports | `get_all_shops()` in `database.py`; `apply_filters()` and `show_statistics()` in `gui.py`; `generate_report()` in `report.py` |
| Lists | Hold records returned by the API and iterate over shops | `self.all_shops` and `apply_filters()` in `gui.py`; `generate_report(shops)` in `report.py` |
| Dictionaries | Represent records, form values, JSON responses, and city counts | `get_all_shops()` in `database.py`; form/JSON handling in `app.py`; `city_counts` in `show_statistics()` and `generate_report()` |
| Classes and objects | Organize GUI and database functionality | `CoffeeShopApp` in `gui.py`; `DatabaseManager` in `database.py` |
| Exception handling | Handle invalid ratings, HTTP errors, connection failures, timeouts, and report-worker errors | Route functions in `app.py`; request/CRUD handlers and `report_worker()` in `gui.py` |
| SQLite and SQL | Create the table and perform parameterized CRUD queries | `create_table()`, `add_shop()`, `get_all_shops()`, `get_shop()`, `update_shop()`, and `delete_shop()` in `database.py` |
| Tkinter | Build windows, forms, buttons, labels, filters, and the records table | `create_widgets()`, `create_add_form()`, `edit_shop()`, and `show_statistics()` in `gui.py` |
| Client-server communication | Send GET/POST requests and decode JSON replies | `load_shops()` and `send_post_request()` in `gui.py`; routes in `app.py` |
| Flask | Define API routes, validate submitted fields, and return JSON/status codes | `get_shops()`, `get_shop()`, `add_shop()`, `update_shop()`, and `delete_shop()` in `app.py` |
| File handling | Create and write the UTF-8 report using a `with` statement | `generate_report()` in `report.py` |
| Threading and queues | Run report generation in a daemon worker thread and pass its result to Tkinter | `start_report_generation()`, `report_worker()`, and `check_report_status()` in `gui.py` |
| Functional tools | Use `lambda` as a key function when finding the highest rating | `show_statistics()` in `gui.py`; `generate_report()` in `report.py` |
| Path handling | Build database/report paths and create directories | `DatabaseManager.__init__()` in `database.py`; `generate_report()` in `report.py` |

## Report Generation

To generate a report:

1.  Start Flask using `python app.py`.
2.  Start the GUI using `python gui.py`.
3.  Click **Generate Report** in the Tkinter window.

The report workflow is implemented as follows:

1.  `start_report_generation()` disables the report button, creates a
    `queue.Queue`, creates a daemon `threading.Thread`, starts it with
    `start()`, and schedules a status check using `root.after()`.
2.  `report_worker()` requests the latest records from Flask at
    `/shops`.
3.  The worker calls `generate_report(shops)` from `report.py`.
4.  `generate_report()` calculates the total number of shops, average
    rating, highest-rated shop, and shop counts by city. It writes the
    statistics and all records to a UTF-8 text file using
    `with open(...)`.
5.  The worker places a success or error result in the queue.
6.  `check_report_status()` checks the queue. When a result is
    available, it calls `join()`, re-enables the report button, and
    displays the result. If the worker is still running, it schedules
    another check with `root.after()`.

The generated file is:

``` text
reports/coffee_report.txt
```

The `reports` directory is created automatically if it does not exist.
Errors raised during the worker workflow are caught in `report_worker()`
and returned to the GUI for display.

## Testing

The project includes two test scripts. Run them from the project root
with the virtual environment activated.

### 1. API test

Start Flask first in a separate terminal:

``` bash
python app.py
```

Then, in another terminal, run:

``` bash
python test_api.py
```

`test_api.py` sends requests to exercise these operations:

- Add a coffee shop.
- Update the newly added coffee shop.
- Submit an invalid rating (`10`) and inspect the validation response.
- Delete the newly added coffee shop.
- Request an unknown shop ID.
- Retrieve and display the remaining coffee shops.

The script prints HTTP statuses and JSON responses for inspection. It is
a manual test script; it does not use an automated assertion framework.

### 2. Connection test

With Flask running, execute:

``` bash
python test_connection.py
```

This checks whether `http://127.0.0.1:5050/shops` responds within five
seconds. It prints a success message and response status if the server
is reachable, or a timeout/unavailable message otherwise.

### 3. GUI and persistence checks

Manually verify the following behaviors in the desktop application:

- Add, edit, and delete a coffee shop.
- Search by name and filter by city/category.
- Clear the search and filters.
- Open the statistics dashboard.
- Try Edit or Delete without selecting a row.
- Try missing required fields and an invalid rating.
- Stop Flask and use Refresh to confirm that a connection error is
    displayed; restart Flask and refresh again.
- Generate a report and inspect `reports/coffee_report.txt`.
- Restart the applications and confirm that database records remain.

### Test results record

| Test | Result | Notes |
|---|---|---|
| API: add shop | Pass | Run `python test_api.py` |
| API: update shop | Pass | Run `python test_api.py` |
| API: invalid rating | Pass | Confirm HTTP 400 |
| API: delete shop | Pass | Run `python test_api.py` |
| API: unknown ID | Pass | Confirm HTTP 404 |
| Server connection | Pass | Run `python test_connection.py` |
| GUI: CRUD and filters | Pass | Verify through Tkinter |
| GUI: server unavailable/recovery | Pass | Stop and restart Flask |
| Database persistence | Pass | Restart both programs |
| Report generation | Pass | Check `reports/coffee_report.txt` |


## Credits and AI Assistance

- Flask and Python documentation were used as technical references.
- OpenAI ChatGPT was used as an AI-assisted learning and development
    tool for explanations, debugging support, code suggestions, and
    README preparation.
- The student is responsible for reviewing, understanding,
    integrating, and testing the submitted code.


## Author

- **Student name:** Mazen Hassan Bafaqih
- **Student ID:** 443043723
- **Course:** Advanced Programming
- **GitHub:** https://github.com/Mazzz10/MyCoffeeJournal


