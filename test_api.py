
import json

# Encode POST form data
from urllib.parse import urlencode

# Send HTTP requests
from urllib.request import urlopen, Request

# Handle HTTP and connection errors
from urllib.error import HTTPError, URLError

# Used to handle connection timeouts
import socket 

# Flask server address
BASE_URL = "http://127.0.0.1:5050"



def send_request(url, method="GET", values=None):
    """Send an HTTP request and handle connection errors."""

    try:
        # Prepare POST data if values were provided
        if values is not None:
            body = urlencode(values).encode("utf-8")

            # Create POST request
            request = Request(url, data=body, method=method)

        else:
            # Create GET request
            request = Request(url, method=method)

        # Send request with a maximum wait of 5 seconds
        with urlopen(request, timeout=5) as response:

            # Decode the JSON response
            result = json.loads(
                response.read().decode("utf-8")
            )

            print("HTTP Status:", response.status)
            return result

    except HTTPError as error:
        # Handle HTTP errors returned by Flask (400, 404, etc.)
        print("HTTP Error:", error.code)

        return json.loads(
            error.read().decode("utf-8")
        )

    except socket.timeout:
        # Handle requests that take longer than 5 seconds
        print("Connection timed out.")

    except URLError as error:
        # Handle unavailable Flask server or connection problems
        print("Connection failed:", error.reason)

    return None



# ==========================================
# 1. ADD A COFFEE SHOP
# ==========================================

print("\n1. ADD COFFEE SHOP")

new_shop = {
    "name": "Camel Step",
    "city": "Madinah",
    "rating": "4.7",
    "category": "Specialty",
    "notes": "Excellent coffee"
}

result = send_request(
    BASE_URL + "/shops/add",
    method="POST",
    values=new_shop
)

print(result)

# Save the new shop ID for later operations
shop_id = result["id"] if result and result.get("success") else None


# ==========================================
# 2. UPDATE THE COFFEE SHOP
# ==========================================

if shop_id is not None:

    print("\n2. UPDATE COFFEE SHOP")

    updated_shop = {
        "name": "Camel Step Updated",
        "city": "Riyadh",
        "rating": "4.9",
        "category": "Specialty",
        "notes": "Updated review"
    }

    result = send_request(
        f"{BASE_URL}/shops/update/{shop_id}",
        method="POST",
        values=updated_shop
    )

    print(result)


# ==========================================
# 3. TEST INVALID INPUT
# ==========================================

print("\n3. TEST INVALID RATING")

invalid_shop = {
    "name": "Test Cafe",
    "city": "Madinah",
    "rating": "10",
    "category": "Specialty",
    "notes": "Testing validation"
}

result = send_request(
    BASE_URL + "/shops/add",
    method="POST",
    values=invalid_shop
)

print(result)


# ==========================================
# 4. DELETE THE COFFEE SHOP
# ==========================================

if shop_id is not None:

    print("\n4. DELETE COFFEE SHOP")

    result = send_request(
        f"{BASE_URL}/shops/delete/{shop_id}",
        method="POST"
    )

    print(result)


# ==========================================
# 5. TEST UNKNOWN ID
# ==========================================

print("\n5. TEST UNKNOWN ID")

result = send_request(
    BASE_URL + "/shops/999999"
)

print(result)


# ==========================================
# 6. VIEW ALL REMAINING SHOPS
# ==========================================

print("\n6. REMAINING COFFEE SHOPS")

result = send_request(BASE_URL + "/shops")

print(result)
