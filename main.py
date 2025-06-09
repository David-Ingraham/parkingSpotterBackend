from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from routes import register_routes
from waitress import serve
from database.db import init_db

app = Flask(__name__)
CORS(app)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

load_dotenv()

# Initialize database
print("Initializing database...")
init_db()

# Register routes
register_routes(app)

if __name__ == "__main__":
    print("Starting HTTP server on http://0.0.0.0:8000")
    serve(app, host="0.0.0.0", port=8000)
