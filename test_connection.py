
from urllib.request import urlopen
from urllib.error import URLError
import socket

# Flask server address
URL = "http://127.0.0.1:5050/shops"


def test_connection():

    try:
        # Try to contact Flask with a 5-second timeout
        with urlopen(URL, timeout=5) as response:
            print("Server is available!")
            print(response.status)

    except socket.timeout:
        print("Connection timed out!")

    except URLError:
        print("Flask server is unavailable!")


# Run the connection test
test_connection()
