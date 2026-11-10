
from database import DatabaseManager

# Initialize the database manager
db = DatabaseManager()

# ----------------------------------
# 1. ADD: Insert a new coffee shop
# ----------------------------------

shop_id = db.add_shop(
    name="Brew 92",
    city="Madinah",
    rating=4.5,
    category="Specialty",
    notes="Good coffee and atmosphere"
)

print("Added shop ID:", shop_id)


# ----------------------------------
# 2. READ: Retrieve all coffee shops
# ----------------------------------

print("\nAll coffee shops:")

shops = db.get_all_shops()

for shop in shops:
    print(shop)


# ----------------------------------
# 3. READ: Retrieve one coffee shop
# ----------------------------------

print("\nRetrieve one coffee shop:")

shop = db.get_shop(shop_id)

if shop:
    print(shop)
else:
    print("Coffee shop not found!")


# ----------------------------------
# 4. UPDATE: Modify a coffee shop
# ----------------------------------

print("\nUpdating coffee shop:")

updated = db.update_shop(
    shop_id=shop_id,
    name="Brew 92 Updated",
    city="Riyadh",
    rating=4.8,
    category="Specialty",
    notes="Updated information"
)

print("Update successful!" if updated else "Shop not found!")


# ----------------------------------
# 5. DELETE: Remove a coffee shop
# ----------------------------------

print("\nDeleting coffee shop:")

deleted = db.delete_shop(shop_id)

print("Delete successful!" if deleted else "Shop not found!")


# ----------------------------------
# 6. VERIFY: Check remaining records
# ----------------------------------

print("\nRemaining coffee shops:")

for shop in db.get_all_shops():
    print(shop)
