
import tkinter as tk
from tkinter import ttk, messagebox

import json
import socket

# Tools for sending HTTP requests
from urllib.request import urlopen
from urllib.error import HTTPError, URLError


# Flask backend address
BASE_URL = "http://127.0.0.1:5050"


class CoffeeShopApp:

    def __init__(self, root):
        # Store the main Tkinter window
        self.root = root

        # Configure the application window
        self.root.title("Saudi Coffee Shop Guide")
        self.root.geometry("1050x650")
        self.root.minsize(850, 500)

        # Set the application background color
        self.root.configure(bg="#F5F3EE")

        # Configure the table appearance
        self.configure_styles()

        # Build the interface
        self.create_widgets()

        # Load coffee shops from Flask when the app starts
        self.load_shops()

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
            text="Saudi Coffee Shop Guide",
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

        toolbar = tk.Frame(
            main_frame,
            bg="#F5F3EE"
        )
        toolbar.pack(fill="x", pady=(0, 12))

        tk.Label(
            toolbar,
            text="Coffee Shop Records",
            font=("Arial", 15, "bold"),
            bg="#F5F3EE",
            fg="#244A3B"
        ).pack(side="left")

        # Refresh button
        refresh_button = tk.Button(
            toolbar,
            text="Refresh",
            font=("Arial", 10, "bold"),
            bg="#244A3B",
            fg="white",
            activebackground="#315E4B",
            activeforeground="white",
            relief="flat",
            padx=15,
            pady=7,
            command=self.load_shops
        )
        refresh_button.pack(side="right")

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

            # Get the list of coffee shops
            shops = result["data"]

            # Insert each coffee shop into the table
            for shop in shops:
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

            # Update the total number of coffee shops
            self.total_label.config(text=str(len(shops)))

            # Update the status message
            self.status_label.config(
                text=f"Connected successfully | {len(shops)} shops loaded",
                fg="#244A3B"
            )

        except HTTPError as error:
            # Handle HTTP errors returned by Flask
            self.status_label.config(
                text=f"Server error: HTTP {error.code}",
                fg="red"
            )

        except URLError:
            # Handle unavailable Flask server
            self.status_label.config(
                text="Connection failed. Make sure Flask is running.",
                fg="red"
            )

        except socket.timeout:
            # Handle connection timeout
            self.status_label.config(
                text="Connection timed out. Please try again.",
                fg="red"
            )

        except (ValueError, KeyError, json.JSONDecodeError):
            # Handle invalid or unexpected server responses
            self.status_label.config(
                text="Invalid response received from server.",
                fg="red"
            )


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
