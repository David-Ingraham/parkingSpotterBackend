from flask import Flask, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
from routes import register_routes
from waitress import serve
from database.db import init_db

app = Flask(__name__)
CORS(app)

# Add cache control headers for static files
@app.after_request
def add_header(response):
    if 'Cache-Control' not in response.headers:
        response.headers['Cache-Control'] = 'public, max-age=60'  # Cache for 1 minute
    return response

load_dotenv()

# Initialize database
print("Initializing database...")
init_db()

# Register routes
register_routes(app)

if __name__ == "__main__":
    print("Starting HTTP server on http://0.0.0.0:8000")
    serve(app, host="0.0.0.0", port=8000)
