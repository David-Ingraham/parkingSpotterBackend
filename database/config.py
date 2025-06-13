import os

# Database configuration
DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'postgres')
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '5432')
DB_NAME = os.getenv('DB_NAME', 'parking_spotter')

# Debug logging to see what we actually got
print(f"DEBUG: DB_USER = '{DB_USER}'")
print(f"DEBUG: DB_PASSWORD = '{'*' * len(DB_PASSWORD) if DB_PASSWORD else 'None'}'")
print(f"DEBUG: DB_HOST = '{DB_HOST}'")
print(f"DEBUG: DB_PORT = '{DB_PORT}'")
print(f"DEBUG: DB_NAME = '{DB_NAME}'")

# Database URL
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
print(f"DEBUG: DATABASE_URL = postgresql://{DB_USER}:***@{DB_HOST}:{DB_PORT}/{DB_NAME}")

# Other configurations can be added here
WEBSOCKET_PORT = 8001
HTTP_PORT = 8000 