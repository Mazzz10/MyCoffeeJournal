
from database import DatabaseManager

# Create database object
db = DatabaseManager()

# Add a coffee shop
shop_id = db.add_shop(
    name="Brew 92",
    city="Madinah",
    rating=4.5,
    category="Specialty",
    notes="Good coffee and atmosphere"
)

print("Added shop with ID:", shop_id)

# Retrieve all coffee shops
shops = db.get_all_shops()

print("\nAll Coffee Shops:")

for shop in shops:
    print(shop)
