
from flask import Flask, request, jsonify

# Import our database class
from database import DatabaseManager

# Create the Flask application
app = Flask(__name__)

# Create the database manager
# This also ensures that the database table exists
db = DatabaseManager()


# ------------------------------------------
# GET: Retrieve all coffee shops
# ------------------------------------------

@app.route("/shops", methods=["GET"])
def get_shops():

    try:
        # Retrieve all records from SQLite
        shops = db.get_all_shops()

        # Return the records as JSON
        return jsonify({
            "success": True,
            "data": shops
        }), 200

    except Exception:
        # Return an error if something goes wrong
        app.logger.exception("Failed to retrieve shops")

        return jsonify({
            "success": False,
            "message": "Failed to retrieve coffee shops"
        }), 500


# ------------------------------------------
# GET: Retrieve one coffee shop by ID
# ------------------------------------------

@app.route("/shops/<int:shop_id>", methods=["GET"])
def get_shop(shop_id):

    try:
        # Search for the requested shop
        shop = db.get_shop(shop_id)

        # Check whether the shop exists
        if shop is None:
            return jsonify({
                "success": False,
                "message": "Coffee shop not found"
            }), 404

        return jsonify({
            "success": True,
            "data": shop
        }), 200

    except Exception:
        app.logger.exception("Failed to retrieve shop")

        return jsonify({
            "success": False,
            "message": "Failed to retrieve coffee shop"
        }), 500


# ------------------------------------------
# POST: Add a new coffee shop
# ------------------------------------------

@app.route("/shops/add", methods=["POST"])
def add_shop():

    # Get submitted form values
    name = request.form.get("name", "").strip()
    city = request.form.get("city", "").strip()
    rating = request.form.get("rating", "").strip()
    category = request.form.get("category", "").strip()
    notes = request.form.get("notes", "").strip()

    # Validate required fields
    if not name or not city or not rating or not category:
        return jsonify({
            "success": False,
            "message": "Name, city, rating and category are required"
        }), 400

    # Convert rating into a number
    try:
        rating = float(rating)
    except ValueError:
        return jsonify({
            "success": False,
            "message": "Rating must be a number"
        }), 400

    # Check rating range
    if not 0 <= rating <= 5:
        return jsonify({
            "success": False,
            "message": "Rating must be between 0 and 5"
        }), 400

    try:
        # Save the coffee shop in SQLite
        shop_id = db.add_shop(
            name, city, rating, category, notes
        )

        return jsonify({
            "success": True,
            "message": "Coffee shop added successfully",
            "id": shop_id
        }), 201

    except Exception:
        app.logger.exception("Failed to add shop")

        return jsonify({
            "success": False,
            "message": "Failed to add coffee shop"
        }), 500


# ------------------------------------------
# POST: Update an existing coffee shop
# ------------------------------------------

@app.route("/shops/update/<int:shop_id>", methods=["POST"])
def update_shop(shop_id):

    # Get submitted form values
    name = request.form.get("name", "").strip()
    city = request.form.get("city", "").strip()
    rating = request.form.get("rating", "").strip()
    category = request.form.get("category", "").strip()
    notes = request.form.get("notes", "").strip()

    # Validate required fields
    if not name or not city or not rating or not category:
        return jsonify({
            "success": False,
            "message": "Required fields are missing"
        }), 400

    # Validate rating
    try:
        rating = float(rating)
    except ValueError:
        return jsonify({
            "success": False,
            "message": "Rating must be a number"
        }), 400

    if not 0 <= rating <= 5:
        return jsonify({
            "success": False,
            "message": "Rating must be between 0 and 5"
        }), 400

    try:
        # Update the selected coffee shop
        updated = db.update_shop(
            shop_id, name, city, rating, category, notes
        )

        # Check whether the record exists
        if not updated:
            return jsonify({
                "success": False,
                "message": "Coffee shop not found"
            }), 404

        return jsonify({
            "success": True,
            "message": "Coffee shop updated successfully"
        }), 200

    except Exception:
        app.logger.exception("Failed to update shop")

        return jsonify({
            "success": False,
            "message": "Failed to update coffee shop"
        }), 500


# ------------------------------------------
# POST: Delete a coffee shop
# ------------------------------------------

@app.route("/shops/delete/<int:shop_id>", methods=["POST"])
def delete_shop(shop_id):

    try:
        # Delete the selected coffee shop
        deleted = db.delete_shop(shop_id)

        # Check whether the record existed
        if not deleted:
            return jsonify({
                "success": False,
                "message": "Coffee shop not found"
            }), 404

        return jsonify({
            "success": True,
            "message": "Coffee shop deleted successfully"
        }), 200

    except Exception:
        app.logger.exception("Failed to delete shop")

        return jsonify({
            "success": False,
            "message": "Failed to delete coffee shop"
        }), 500


# ------------------------------------------
# Start the Flask server
# ------------------------------------------

if __name__ == "__main__":

    # Run Flask on localhost using port 5050
    app.run(host="127.0.0.1", port=5050, debug=False)
