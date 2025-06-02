from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv

from waitress import serve
from routes import register_routes  # you'll create this

app = Flask(__name__, static_url_path='/static', static_folder='static')
CORS(app)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

load_dotenv()

register_routes(app)

if __name__ == "__main__":
    serve(app, host='0.0.0.0', port=8000)
