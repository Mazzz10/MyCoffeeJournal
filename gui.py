import tkinter as tk
from tkinter import ttk, messagebox

# Used to create a background worker thread
import threading

# Used to safely send results from the worker to Tkinter
import queue

# Import our report generation function
from report import generate_report

import json
import socket

# Tools for sending HTTP requests
from urllib.request import urlopen
from urllib.error import HTTPError, URLError

# Used to encode POST form data
from urllib.parse import urlencode

# Used to create HTTP POST requests
from urllib.request import Request


# Flask backend address
BASE_URL = "http://127.0.0.1:5050"


class CoffeeShopApp:

    def __init__(self, root):
        # Store the main Tkinter window
        self.root = root

        # Configure the application window
        self.root.title("My Coffee Journal")
        self.root.geometry("1050x650")
        self.root.minsize(850, 500)

        # Set the application background color
        self.root.configure(bg="#F5F3EE")

        # Configure the table appearance
        self.configure_styles()

        # Store all coffee shops retrieved from Flask
        # Filtering will use this list without repeatedly contacting Flask
        self.all_shops = []

        # Build the interface
        self.create_widgets()


        # Load coffee shops from Flask when the app starts
        self.load_shops()


    def create_add_form(self):
        """Open a window for adding a new coffee shop."""

        # Create a separate window
        form_window = tk.Toplevel(self.root)
        form_window.title("Add Coffee Shop")
        form_window.geometry("450x550")
        form_window.configure(bg="#F5F3EE")
        form_window.resizable(False, False)

        # Store form inputs so save_shop() can access them
        self.form_window = form_window

        # Main form container
        form_frame = tk.Frame(
            form_window,
            bg="#F5F3EE",
            padx=25,
            pady=20
        )
        form_frame.pack(fill="both", expand=True)

        # Form title
        tk.Label(
            form_frame,
            text="Add New Coffee Shop",
            font=("Arial", 18, "bold"),
            bg="#F5F3EE",
            fg="#244A3B"
        ).pack(anchor="w", pady=(0, 20))

        # -------------------------------
        # SHOP NAME
        # -------------------------------

        tk.Label(
            form_frame,
            text="Shop Name *",
            bg="#F5F3EE",
            font=("Arial", 10, "bold")
        ).pack(anchor="w")

        self.name_entry = tk.Entry(
            form_frame,
            font=("Arial", 11)
        )
        self.name_entry.pack(fill="x", pady=(5, 15))

        # -------------------------------
        # CITY
        # -------------------------------

        tk.Label(
            form_frame,
            text="City *",
            bg="#F5F3EE",
            font=("Arial", 10, "bold")
        ).pack(anchor="w")

        self.city_entry = ttk.Combobox(
            form_frame,
            values=[
                "Madinah",
                "Riyadh",
                "Jeddah",
                "Makkah",
                "Dammam",
                "Khobar",
                "Taif",
                "Abha"
            ],
            state="readonly",
            font=("Arial", 10)
        )
        self.city_entry.pack(fill="x", pady=(5, 15))

        # -------------------------------
        # RATING
        # -------------------------------

        tk.Label(
            form_frame,
            text="Rating (0 - 5) *",
            bg="#F5F3EE",
            font=("Arial", 10, "bold")
        ).pack(anchor="w")

        self.rating_entry = tk.Entry(
            form_frame,
            font=("Arial", 11)
        )
        self.rating_entry.pack(fill="x", pady=(5, 15))

        # -------------------------------
        # CATEGORY
        # -------------------------------

        tk.Label(
            form_frame,
            text="Category *",
            bg="#F5F3EE",
            font=("Arial", 10, "bold")
        ).pack(anchor="w")

        self.category_entry = ttk.Combobox(
            form_frame,
            values=[
                "Specialty",
                "Traditional",
                "International",
                "Other"
            ],
            state="readonly",
            font=("Arial", 10)
        )
        self.category_entry.pack(fill="x", pady=(5, 15))

        # -------------------------------
        # NOTES
        # -------------------------------

        tk.Label(
            form_frame,
            text="Notes",
            bg="#F5F3EE",
            font=("Arial", 10, "bold")
        ).pack(anchor="w")

        self.notes_entry = tk.Text(
            form_frame,
            height=4,
            font=("Arial", 10)
        )
        self.notes_entry.pack(fill="x", pady=(5, 20))

        # -------------------------------
        # SAVE BUTTON
        # -------------------------------

        tk.Button(
            form_frame,
            text="Save Coffee Shop",
            bg="#244A3B",
            fg="white",
            font=("Arial", 11, "bold"),
            relief="flat",
            command=self.save_shop
        ).pack(fill="x", ipady=8)

    def send_post_request(self, endpoint, values):
        """Send form data to a Flask POST endpoint."""

        # Convert the dictionary into URL-encoded bytes
        body = urlencode(values).encode("utf-8")

        # Create a POST request
        request = Request(
            BASE_URL + endpoint,
            data=body,
            method="POST"
        )

        # Send the request and decode the JSON response
        with urlopen(request, timeout=5) as response:
            return json.loads(
                response.read().decode("utf-8")
            )

    def save_shop(self):
        """Validate form data and save a coffee shop."""

        # Collect values from the form
        name = self.name_entry.get().strip()
        city = self.city_entry.get().strip()
        rating = self.rating_entry.get().strip()
        category = self.category_entry.get().strip()
        notes = self.notes_entry.get("1.0", "end-1c").strip()

        # Check required fields
        if not name or not city or not rating or not category:
            messagebox.showwarning(
                "Missing Information",
                "Please fill in all required fields."
            )
            return

        # Validate rating before sending it to Flask
        try:
            rating_value = float(rating)

            if not 0 <= rating_value <= 5:
                raise ValueError

        except ValueError:
            messagebox.showerror(
                "Invalid Rating",
                "Rating must be a number between 0 and 5."
            )
            return

        # Prepare data for the Flask backend
        values = {
            "name": name,
            "city": city,
            "rating": rating,
            "category": category,
            "notes": notes
        }

        try:
            # Send the POST request to Flask
            result = self.send_post_request(
                "/shops/add",
                values
            )

            # Check the server response
            if result.get("success"):

                messagebox.showinfo(
                    "Success",
                    "Coffee shop added successfully!"
                )

                # Close the form
                self.form_window.destroy()

                # Refresh the main table
                self.load_shops()

        except HTTPError as error:
            # Read and display Flask's error response
            error_data = json.loads(
                error.read().decode("utf-8")
            )

            messagebox.showerror(
                "Server Error",
                error_data.get("message", "Request failed")
            )

        except (URLError, socket.timeout):
            # Handle unavailable server or timeout
            messagebox.showerror(
                "Connection Error",
                "Cannot connect to Flask. Please check the server."
            )


    def configure_styles(self):
        """Configure the appearance of Tkinter widgets."""

        style = ttk.Style()

        # Use the native theme as a base
        style.theme_use("clam")

        # Configure table headings
        style.configure(
            "Treeview.Heading",
            font=("Arial", 10, "bold"),
            background="#244A3B",
            foreground="white",
            padding=10
        )

        # Configure table rows
        style.configure(
            "Treeview",
            font=("Arial", 10),
            rowheight=35,
            background="white",
            fieldbackground="white"
        )

        # Configure selected table row
        style.map(
            "Treeview",
            background=[("selected", "#A9C5B5")],
            foreground=[("selected", "#172E25")]
        )

    def create_widgets(self):
        """Create the main application interface."""

        # Main container
        main_frame = tk.Frame(
            self.root,
            bg="#F5F3EE",
            padx=30,
            pady=25
        )
        main_frame.pack(fill="both", expand=True)

        # --------------------------------
        # HEADER
        # --------------------------------

        header_frame = tk.Frame(
            main_frame,
            bg="#F5F3EE"
        )
        header_frame.pack(fill="x", pady=(0, 20))

        # Application title
        title = tk.Label(
            header_frame,
            text="My Coffee Journal",
            font=("Arial", 22, "bold"),
            bg="#F5F3EE",
            fg="#244A3B"
        )
        title.pack(anchor="w")

        # Application description
        subtitle = tk.Label(
            header_frame,
            text="Discover and manage your favorite coffee shops",
            font=("Arial", 10),
            bg="#F5F3EE",
            fg="#666666"
        )
        subtitle.pack(anchor="w", pady=(5, 0))

        # --------------------------------
        # STATISTICS AREA
        # --------------------------------

        stats_frame = tk.Frame(
            main_frame,
            bg="white",
            padx=20,
            pady=15
        )
        stats_frame.pack(fill="x", pady=(0, 20))

        tk.Label(
            stats_frame,
            text="TOTAL COFFEE SHOPS",
            font=("Arial", 10, "bold"),
            bg="white",
            fg="#666666"
        ).pack(anchor="w")

        # Display the number of saved coffee shops
        self.total_label = tk.Label(
            stats_frame,
            text="0",
            font=("Arial", 24, "bold"),
            bg="white",
            fg="#244A3B"
        )
        self.total_label.pack(anchor="w")

        
        # --------------------------------
        # TOOLBAR
        # --------------------------------

        # Create the toolbar inside the main window
        toolbar = tk.Frame(
            main_frame,
            bg="#F5F3EE"
        )
        toolbar.pack(fill="x", pady=(0, 12))

        # Section title
        tk.Label(
            toolbar,
            text="Coffee Shop Records",
            font=("Arial", 15, "bold"),
            bg="#F5F3EE",
            fg="#244A3B"
        ).pack(side="left")

        # Create a container for the buttons
        button_frame = tk.Frame(
            toolbar,
            bg="#F5F3EE"
        )
        button_frame.pack(side="right")

        # Add Coffee Shop button
        add_button = tk.Button(
            button_frame,
            text="+ Add Coffee Shop",
            font=("Arial", 10, "bold"),
            bg="#244A3B",
            fg="white",
            relief="flat",
            padx=15,
            pady=7,
            command=self.create_add_form
        )
        add_button.pack(side="left", padx=(0, 8))

        # Refresh button
        refresh_button = tk.Button(
            button_frame,
            text="Refresh",
            font=("Arial", 10, "bold"),
            bg="#244A3B",
            fg="white",
            relief="flat",
            padx=15,
            pady=7,
            command=self.load_shops
        )
        refresh_button.pack(side="left")

        # Statistics dashboard button
        statistics_button = tk.Button(
            button_frame,
            text="Statistics",
            font=("Arial", 10, "bold"),
            bg="#527A68",
            fg="white",
            relief="flat",
            padx=15,
            pady=7,
            command=self.show_statistics
        )
        statistics_button.pack(side="left", padx=(8, 0))


        # Generate Report button
        self.report_button = tk.Button(
            button_frame,
            text="Generate Report",
            font=("Arial", 10, "bold"),
            bg="#527A68",
            fg="white",
            relief="flat",
            padx=15,
            pady=7,
            command=self.start_report_generation
        )

        # Display the report button
        self.report_button.pack(side="left", padx=(8, 0))


        # Edit selected coffee shop button
        edit_button = tk.Button(
            button_frame,
            text="Edit",
            font=("Arial", 10, "bold"),
            bg="#D69E36",
            fg="white",
            relief="flat",
            padx=15,
            pady=7,
            command=self.edit_shop
        )
        edit_button.pack(side="left", padx=(0, 8))

        # Delete selected coffee shop button
        delete_button = tk.Button(
            button_frame,
            text="Delete",
            font=("Arial", 10, "bold"),
            bg="#B84040",
            fg="white",
            relief="flat",
            padx=15,
            pady=7,
            command=self.delete_shop
        )
        delete_button.pack(side="left")


        # --------------------------------
        # SEARCH AND FILTER SECTION
        # --------------------------------

        # Container for search and filter controls
        filter_frame = tk.Frame(
            main_frame,
            bg="#F5F3EE"
        )
        filter_frame.pack(fill="x", pady=(0, 12))

        # Search input
        self.search_entry = tk.Entry(
            filter_frame,
            font=("Arial", 10),
            width=30
        )
        self.search_entry.pack(
            side="left",
            padx=(0, 10),
            ipady=6
        )

        # Search when the user types
        self.search_entry.bind(
            "<KeyRelease>",
            lambda event: self.apply_filters()
        )

        # City filter
        self.city_filter = ttk.Combobox(
            filter_frame,
            values=[
                "All Cities",
                "Madinah",
                "Riyadh",
                "Jeddah",
                "Makkah",
                "Dammam",
                "Khobar",
                "Taif",
                "Abha"
            ],
            state="readonly",
            width=15
        )
        self.city_filter.pack(side="left", padx=5)

        # Set the default city filter
        self.city_filter.set("All Cities")

        # Apply filters whenever the city changes
        self.city_filter.bind(
            "<<ComboboxSelected>>",
            lambda event: self.apply_filters()
        )

        # Category filter
        self.category_filter = ttk.Combobox(
            filter_frame,
            values=[
                "All Categories",
                "Specialty",
                "Traditional",
                "International",
                "Other"
            ],
            state="readonly",
            width=17
        )
        self.category_filter.pack(side="left", padx=5)

        # Set the default category filter
        self.category_filter.set("All Categories")

        # Apply filters whenever the category changes
        self.category_filter.bind(
            "<<ComboboxSelected>>",
            lambda event: self.apply_filters()
        )

        # Clear all filters button
        clear_button = tk.Button(
            filter_frame,
            text="Clear Filters",
            font=("Arial", 9, "bold"),
            bg="#D69E36",
            fg="white",
            relief="flat",
            padx=12,
            pady=6,
            command=self.clear_filters
        )
        clear_button.pack(side="right")




        # --------------------------------
        # COFFEE SHOP TABLE
        # --------------------------------

        table_frame = tk.Frame(main_frame, bg="white")
        table_frame.pack(fill="both", expand=True)

        # Define the table columns
        columns = (
            "id",
            "name",
            "city",
            "rating",
            "category",
            "notes"
        )

        # Create the Treeview table
        self.shop_table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings"
        )

        # Configure column headings
        self.shop_table.heading("id", text="ID")
        self.shop_table.heading("name", text="Name")
        self.shop_table.heading("city", text="City")
        self.shop_table.heading("rating", text="Rating")
        self.shop_table.heading("category", text="Category")
        self.shop_table.heading("notes", text="Notes")

        # Configure column widths
        self.shop_table.column("id", width=50, anchor="center")
        self.shop_table.column("name", width=160)
        self.shop_table.column("city", width=120)
        self.shop_table.column("rating", width=80, anchor="center")
        self.shop_table.column("category", width=120)
        self.shop_table.column("notes", width=300)

        # Add a vertical scrollbar
        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.shop_table.yview
        )

        self.shop_table.configure(
            yscrollcommand=scrollbar.set
        )

        # Display the table and scrollbar
        self.shop_table.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        # --------------------------------
        # STATUS BAR
        # --------------------------------

        self.status_label = tk.Label(
            main_frame,
            text="Connecting to server...",
            font=("Arial", 9),
            bg="#F5F3EE",
            fg="#666666"
        )
        self.status_label.pack(anchor="w", pady=(12, 0))

    def load_shops(self):
        """Retrieve coffee shops from Flask and display them."""

        try:
            # Send a GET request to Flask
            with urlopen(
                BASE_URL + "/shops",
                timeout=5
            ) as response:

                # Decode the JSON response
                result = json.loads(
                    response.read().decode("utf-8")
                )

            # Check whether Flask returned success
            if not result.get("success"):
                raise ValueError("Unable to retrieve coffee shops")

            # Clear existing table rows before refreshing
            for item in self.shop_table.get_children():
                self.shop_table.delete(item)

            # Store all coffee shops retrieved from Flask
            self.all_shops = result["data"]

            # Apply current search and filter settings
            self.apply_filters()

            # Update the total number of coffee shops
            #self.total_label.config(text=str(len(shops)))

            # Update the status message
            # self.status_label.config(
            #     text=f"Connected successfully | {len(shops)} shops loaded",
            #     fg="#244A3B"
            # )

        except HTTPError as error:
            # Handle HTTP errors returned by Flask
            self.status_label.config(
                text=f"Server error: HTTP {error.code}",
                fg="red"
            )

            # Show an error popup
            messagebox.showerror(
                "Server Error",
                f"Flask returned an error: HTTP {error.code}"
            )

        except socket.timeout:
            # Handle requests that take too long
            self.status_label.config(
                text="Connection timed out.",
                fg="red"
            )

            # Inform the user about the timeout
            messagebox.showerror(
                "Connection Timeout",
                "The Flask server did not respond in time."
            )

        except URLError as error:
            # Handle unavailable Flask server
            self.status_label.config(
                text="Connection failed. Flask is unavailable.",
                fg="red"
            )

            # Show the connection error
            messagebox.showerror(
                "Connection Error",
                "Cannot connect to Flask!\n\n"
                "Make sure the Flask server is running."
            )

        except (ValueError, KeyError, json.JSONDecodeError):
            # Handle unexpected or invalid server responses
            self.status_label.config(
                text="Invalid response received from server.",
                fg="red"
            )

            messagebox.showerror(
                "Response Error",
                "The server returned an invalid response."
            )

    def edit_shop(self):
        """Open the selected coffee shop for editing."""

        # Get the selected row from the table
        selected = self.shop_table.selection()

        # Make sure a record is selected
        if not selected:
            messagebox.showwarning(
                "No Selection",
                "Please select a coffee shop to edit."
            )
            return

        # Retrieve the selected row values
        values = self.shop_table.item(selected[0], "values")

        # Extract the coffee shop ID
        shop_id = int(values[0])

        # Create the edit window
        edit_window = tk.Toplevel(self.root)
        edit_window.title("Edit Coffee Shop")
        edit_window.geometry("450x550")
        edit_window.configure(bg="#F5F3EE")
        edit_window.resizable(False, False)

        # Main form container
        form_frame = tk.Frame(
            edit_window,
            bg="#F5F3EE",
            padx=25,
            pady=20
        )
        form_frame.pack(fill="both", expand=True)

        # Form title
        tk.Label(
            form_frame,
            text="Edit Coffee Shop",
            font=("Arial", 18, "bold"),
            bg="#F5F3EE",
            fg="#244A3B"
        ).pack(anchor="w", pady=(0, 20))

        # Shop name
        tk.Label(
            form_frame,
            text="Shop Name *",
            bg="#F5F3EE"
        ).pack(anchor="w")

        name_entry = tk.Entry(form_frame, font=("Arial", 11))
        name_entry.pack(fill="x", pady=(5, 15))
        name_entry.insert(0, values[1])

        # City
        tk.Label(
            form_frame,
            text="City *",
            bg="#F5F3EE"
        ).pack(anchor="w")

        city_entry = ttk.Combobox(
            form_frame,
            values=[
                "Madinah", "Riyadh", "Jeddah", "Makkah",
                "Dammam", "Khobar", "Taif", "Abha"
            ],
            state="readonly"
        )
        city_entry.pack(fill="x", pady=(5, 15))
        city_entry.set(values[2])

        # Rating
        tk.Label(
            form_frame,
            text="Rating (0 - 5) *",
            bg="#F5F3EE"
        ).pack(anchor="w")

        rating_entry = tk.Entry(form_frame, font=("Arial", 11))
        rating_entry.pack(fill="x", pady=(5, 15))
        rating_entry.insert(0, values[3])

        # Category
        tk.Label(
            form_frame,
            text="Category *",
            bg="#F5F3EE"
        ).pack(anchor="w")

        category_entry = ttk.Combobox(
            form_frame,
            values=[
                "Specialty",
                "Traditional",
                "International",
                "Other"
            ],
            state="readonly"
        )
        category_entry.pack(fill="x", pady=(5, 15))
        category_entry.set(values[4])

        # Notes
        tk.Label(
            form_frame,
            text="Notes",
            bg="#F5F3EE"
        ).pack(anchor="w")

        notes_entry = tk.Text(form_frame, height=4)
        notes_entry.pack(fill="x", pady=(5, 15))
        notes_entry.insert("1.0", values[5])

        def save_changes():
            """Validate and submit the edited coffee shop."""

            # Collect updated values
            name = name_entry.get().strip()
            city = city_entry.get().strip()
            rating = rating_entry.get().strip()
            category = category_entry.get().strip()
            notes = notes_entry.get("1.0", "end-1c").strip()

            # Validate required fields
            if not name or not city or not rating or not category:
                messagebox.showwarning(
                    "Missing Information",
                    "Please fill in all required fields."
                )
                return

            # Validate rating
            try:
                rating_value = float(rating)

                if not 0 <= rating_value <= 5:
                    raise ValueError

            except ValueError:
                messagebox.showerror(
                    "Invalid Rating",
                    "Rating must be between 0 and 5."
                )
                return

            # Prepare the updated data
            updated_values = {
                "name": name,
                "city": city,
                "rating": rating,
                "category": category,
                "notes": notes
            }

            try:
                # Send POST request to Flask
                result = self.send_post_request(
                    f"/shops/update/{shop_id}",
                    updated_values
                )

                if result.get("success"):
                    messagebox.showinfo(
                        "Success",
                        "Coffee shop updated successfully!"
                    )

                    # Close edit window and refresh table
                    edit_window.destroy()
                    self.load_shops()

            except HTTPError as error:
                # Display error returned by Flask
                error_data = json.loads(
                    error.read().decode("utf-8")
                )

                messagebox.showerror(
                    "Server Error",
                    error_data.get("message", "Update failed")
                )

            except (URLError, socket.timeout):
                # Handle connection problems
                messagebox.showerror(
                    "Connection Error",
                    "Cannot connect to Flask."
                )

        # Save changes button
        tk.Button(
            form_frame,
            text="Save Changes",
            bg="#244A3B",
            fg="white",
            font=("Arial", 11, "bold"),
            relief="flat",
            command=save_changes
        ).pack(fill="x", ipady=8)


    def delete_shop(self):
        """Delete the selected coffee shop after confirmation."""

        # Get the selected row
        selected = self.shop_table.selection()

        # Check whether the user selected a record
        if not selected:
            messagebox.showwarning(
                "No Selection",
                "Please select a coffee shop to delete."
            )
            return

        # Retrieve the selected record
        values = self.shop_table.item(selected[0], "values")

        # Extract the ID and name
        shop_id = int(values[0])
        shop_name = values[1]

        # Ask the user to confirm deletion
        confirm = messagebox.askyesno(
            "Confirm Deletion",
            f"Are you sure you want to delete {shop_name}?"
        )

        # Stop if the user cancels
        if not confirm:
            return

        try:
            # Send POST request to Flask
            result = self.send_post_request(
                f"/shops/delete/{shop_id}",
                {}
            )

            if result.get("success"):

                messagebox.showinfo(
                    "Success",
                    "Coffee shop deleted successfully!"
                )

                # Refresh the table
                self.load_shops()

        except HTTPError as error:
            # Read Flask's error response
            error_data = json.loads(
                error.read().decode("utf-8")
            )

            messagebox.showerror(
                "Server Error",
                error_data.get("message", "Delete failed")
            )

        except (URLError, socket.timeout):
            # Handle connection failure
            messagebox.showerror(
                "Connection Error",
                "Cannot connect to Flask."
            )

    
    def apply_filters(self):
        """Filter coffee shops using name, city and category."""

        # Get the user's search text
        search_text = self.search_entry.get().strip().lower()

        # Get selected city and category
        selected_city = self.city_filter.get()
        selected_category = self.category_filter.get()

        # Clear the current table
        for item in self.shop_table.get_children():
            self.shop_table.delete(item)

        # Loop through all stored coffee shops
        for shop in self.all_shops:

            # Check whether the name matches the search
            name_matches = (
                search_text in shop["name"].lower()
            )

            # Check whether the selected city matches
            city_matches = (
                selected_city == "All Cities"
                or shop["city"] == selected_city
            )

            # Check whether the selected category matches
            category_matches = (
                selected_category == "All Categories"
                or shop["category"] == selected_category
            )

            # Display only records matching all conditions
            if name_matches and city_matches and category_matches:

                self.shop_table.insert(
                    "",
                    "end",
                    values=(
                        shop["id"],
                        shop["name"],
                        shop["city"],
                        shop["rating"],
                        shop["category"],
                        shop["notes"] or ""
                    )
                )

        # Update the total to show the number of visible records
        visible_count = len(self.shop_table.get_children())

        self.total_label.config(text=str(visible_count))

        # Update the status message
        self.status_label.config(
            text=f"Showing {visible_count} matching coffee shops",
            fg="#244A3B"
        )

    def clear_filters(self):
        """Reset all search and filter controls."""

        # Clear the search input
        self.search_entry.delete(0, "end")

        # Reset city and category filters
        self.city_filter.set("All Cities")
        self.category_filter.set("All Categories")

        # Display all coffee shops again
        self.apply_filters()

    
    def show_statistics(self):
        """Display statistics about all saved coffee shops."""

        # Get all coffee shops stored in the application
        shops = self.all_shops

        # Check whether the database contains any records
        if not shops:
            messagebox.showinfo(
                "Statistics",
                "There are no coffee shops to analyze yet."
            )
            return

        # --------------------------------
        # CALCULATE TOTAL SHOPS
        # --------------------------------

        # Count the number of saved coffee shops
        total_shops = len(shops)

        # --------------------------------
        # CALCULATE AVERAGE RATING
        # --------------------------------

        # Extract all ratings and calculate their average
        total_rating = sum(float(shop["rating"]) for shop in shops)

        average_rating = total_rating / total_shops

        # --------------------------------
        # FIND HIGHEST-RATED SHOP
        # --------------------------------

        # Find the coffee shop with the highest rating
        highest_shop = max(
            shops,
            key=lambda shop: float(shop["rating"])
        )

        # --------------------------------
        # COUNT SHOPS BY CITY
        # --------------------------------

        # Dictionary to store city names and their counts
        city_counts = {}

        for shop in shops:

            city = shop["city"]

            # Increase the count for the current city
            city_counts[city] = city_counts.get(city, 0) + 1

        # --------------------------------
        # CREATE STATISTICS WINDOW
        # --------------------------------

        stats_window = tk.Toplevel(self.root)
        stats_window.title("Coffee Shop Statistics")
        stats_window.geometry("550x600")
        stats_window.configure(bg="#F5F3EE")
        stats_window.resizable(False, False)

        # Main container
        stats_frame = tk.Frame(
            stats_window,
            bg="#F5F3EE",
            padx=25,
            pady=25
        )
        stats_frame.pack(fill="both", expand=True)

        # Window title
        tk.Label(
            stats_frame,
            text="Statistics Dashboard",
            font=("Arial", 21, "bold"),
            bg="#F5F3EE",
            fg="#244A3B"
        ).pack(anchor="w", pady=(0, 20))

        # --------------------------------
        # TOTAL SHOPS
        # --------------------------------

        total_frame = tk.Frame(
            stats_frame,
            bg="white",
            padx=15,
            pady=12
        )
        total_frame.pack(fill="x", pady=6)

        tk.Label(
            total_frame,
            text="TOTAL COFFEE SHOPS",
            font=("Arial", 10, "bold"),
            bg="white",
            fg="#666666"
        ).pack(anchor="w")

        tk.Label(
            total_frame,
            text=str(total_shops),
            font=("Arial", 23, "bold"),
            bg="white",
            fg="#244A3B"
        ).pack(anchor="w")

        # --------------------------------
        # AVERAGE RATING
        # --------------------------------

        average_frame = tk.Frame(
            stats_frame,
            bg="white",
            padx=15,
            pady=12
        )
        average_frame.pack(fill="x", pady=6)

        tk.Label(
            average_frame,
            text="AVERAGE RATING",
            font=("Arial", 10, "bold"),
            bg="white",
            fg="#666666"
        ).pack(anchor="w")

        tk.Label(
            average_frame,
            text=f"{average_rating:.2f} / 5",
            font=("Arial", 23, "bold"),
            bg="white",
            fg="#244A3B"
        ).pack(anchor="w")

        # --------------------------------
        # HIGHEST-RATED SHOP
        # --------------------------------

        highest_frame = tk.Frame(
            stats_frame,
            bg="white",
            padx=15,
            pady=12
        )
        highest_frame.pack(fill="x", pady=6)

        tk.Label(
            highest_frame,
            text="HIGHEST-RATED COFFEE SHOP",
            font=("Arial", 10, "bold"),
            bg="white",
            fg="#666666"
        ).pack(anchor="w")

        tk.Label(
            highest_frame,
            text=highest_shop["name"],
            font=("Arial", 15, "bold"),
            bg="white",
            fg="#244A3B"
        ).pack(anchor="w")

        tk.Label(
            highest_frame,
            text=f"Rating: {float(highest_shop['rating']):.1f} / 5",
            font=("Arial", 10),
            bg="white",
            fg="#666666"
        ).pack(anchor="w")

        # --------------------------------
        # SHOPS BY CITY
        # --------------------------------

        city_frame = tk.Frame(
            stats_frame,
            bg="white",
            padx=15,
            pady=12
        )
        city_frame.pack(fill="both", expand=True, pady=6)

        tk.Label(
            city_frame,
            text="COFFEE SHOPS BY CITY",
            font=("Arial", 10, "bold"),
            bg="white",
            fg="#666666"
        ).pack(anchor="w", pady=(0, 10))

        # Display the number of shops in each city
        for city, count in sorted(city_counts.items()):

            tk.Label(
                city_frame,
                text=f"{city}: {count} shop(s)",
                font=("Arial", 11),
                bg="white",
                fg="#244A3B"
            ).pack(anchor="w", pady=3)

    
    def start_report_generation(self):
        """Start report generation in a background thread."""

        # Prevent starting multiple reports simultaneously
        self.report_button.config(state="disabled")

        # Display a status message
        self.status_label.config(
            text="Generating report...",
            fg="#D69E36"
        )

        # Create a queue for communication between threads
        self.report_queue = queue.Queue()

        # Create a worker thread
        self.report_thread = threading.Thread(
            target=self.report_worker,
            daemon=True
        )

        # Start the worker thread
        self.report_thread.start()

        # Check for the worker's result without freezing Tkinter
        self.root.after(100, self.check_report_status)

    def report_worker(self):
        """Retrieve data and generate the report in the worker thread."""

        try:
            # Retrieve all coffee shops from Flask
            with urlopen(BASE_URL + "/shops", timeout=5) as response:

                # Decode the JSON response
                result = json.loads(
                    response.read().decode("utf-8")
                )

            # Check whether Flask returned success
            if not result.get("success"):
                raise ValueError("Could not retrieve coffee shops.")

            # Get all coffee shop records
            shops = result["data"]

            # Generate the text report
            report_path = generate_report(shops)

            # Send the successful result to the main thread
            self.report_queue.put(
                ("success", str(report_path))
            )

        except Exception as error:
            # Send the error message to the main thread
            self.report_queue.put(
                ("error", str(error))
            )

    def check_report_status(self):
        """Check whether the worker thread has finished."""

        # Check whether a result is available
        try:
            status, result = self.report_queue.get_nowait()

            # The worker has finished, so join it safely
            self.report_thread.join()

            # Enable the report button again
            self.report_button.config(state="normal")

            if status == "success":

                # Update the status bar
                self.status_label.config(
                    text="Report generated successfully!",
                    fg="#244A3B"
                )

                # Display the report location
                messagebox.showinfo(
                    "Report Generated",
                    f"Your report was generated successfully!\n\n"
                    f"Location:\n{result}"
                )

            else:

                # Display the error
                self.status_label.config(
                    text="Report generation failed.",
                    fg="red"
                )

                messagebox.showerror(
                    "Report Error",
                    f"Could not generate report:\n{result}"
                )

        except queue.Empty:
            # The worker is still running.
            # Check again after 100 milliseconds.
            self.root.after(100, self.check_report_status)







# --------------------------------
# START THE TKINTER APPLICATION
# --------------------------------

if __name__ == "__main__":

    # Create the main Tkinter window
    root = tk.Tk()

    # Create the application object
    app = CoffeeShopApp(root)

    # Start the Tkinter event loop
    root.mainloop()
