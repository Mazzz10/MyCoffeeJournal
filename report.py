
from pathlib import Path
from datetime import datetime


def generate_report(shops):
    """Generate a text report containing coffee shop information."""

    # --------------------------------
    # CREATE REPORT DIRECTORY
    # --------------------------------

    # Get the project directory
    project_dir = Path(__file__).parent

    # Define the reports folder
    reports_dir = project_dir / "reports"

    # Create the folder if it does not exist
    reports_dir.mkdir(parents=True, exist_ok=True)

    # Define the report file path
    report_path = reports_dir / "coffee_report.txt"

    # --------------------------------
    # CALCULATE STATISTICS
    # --------------------------------

    # Count the total number of coffee shops
    total_shops = len(shops)

    # Calculate average rating and highest-rated shop
    if shops:
        # Extract and sum all ratings
        total_rating = sum(
            float(shop["rating"]) for shop in shops
        )

        # Calculate average rating
        average_rating = total_rating / total_shops

        # Find the shop with the highest rating
        highest_shop = max(
            shops,
            key=lambda shop: float(shop["rating"])
        )

    else:
        # Handle an empty database
        average_rating = 0
        highest_shop = None

    # --------------------------------
    # COUNT SHOPS BY CITY
    # --------------------------------

    # Create a dictionary to store city counts
    city_counts = {}

    for shop in shops:

        # Get the city of the current shop
        city = shop["city"]

        # Increase the city's count
        city_counts[city] = city_counts.get(city, 0) + 1

    # --------------------------------
    # WRITE THE REPORT
    # --------------------------------

    # Open the report file using UTF-8 encoding
    # The "w" mode creates a new file or overwrites an old one
    with open(report_path, "w", encoding="utf-8") as file:

        # Write the report heading
        file.write("=" * 45 + "\n")
        file.write("       SAUDI COFFEE SHOP REPORT\n")
        file.write("=" * 45 + "\n\n")

        # Write the report generation date and time
        file.write(
            f"Generated: {datetime.now():%Y-%m-%d %H:%M:%S}\n\n"
        )

        # Write general statistics
        file.write("GENERAL STATISTICS\n")
        file.write("-" * 45 + "\n")
        file.write(f"Total Coffee Shops: {total_shops}\n")
        file.write(f"Average Rating: {average_rating:.2f} / 5\n\n")

        # Write highest-rated coffee shop information
        file.write("HIGHEST-RATED COFFEE SHOP\n")
        file.write("-" * 45 + "\n")

        if highest_shop:
            file.write(f"Name: {highest_shop['name']}\n")
            file.write(f"City: {highest_shop['city']}\n")
            file.write(
                f"Rating: {float(highest_shop['rating']):.1f} / 5\n\n"
            )
        else:
            file.write("No coffee shops available.\n\n")

        # Write the number of coffee shops in each city
        file.write("COFFEE SHOPS BY CITY\n")
        file.write("-" * 45 + "\n")

        if city_counts:
            for city, count in sorted(city_counts.items()):
                file.write(f"{city}: {count} shop(s)\n")
        else:
            file.write("No city information available.\n")

        # Write all coffee shop records
        file.write("\nALL COFFEE SHOP RECORDS\n")
        file.write("=" * 45 + "\n")

        for shop in shops:

            file.write(f"ID: {shop['id']}\n")
            file.write(f"Name: {shop['name']}\n")
            file.write(f"City: {shop['city']}\n")
            file.write(f"Rating: {shop['rating']}\n")
            file.write(f"Category: {shop['category']}\n")
            file.write(f"Notes: {shop['notes'] or 'None'}\n")

            # Separate each coffee shop record
            file.write("-" * 45 + "\n")

    # Return the path of the generated report
    return report_path
