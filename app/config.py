import os
import dotenv


DEBUG = True

# Load environment variables
dotenv.load_dotenv(verbose=DEBUG)

# Application root directory
ROOT_DIR = os.path.abspath(os.path.dirname(__name__))

# File manager root directory
HOME_DIR = os.path.join(ROOT_DIR, 'home')

# API key stuff
API_KEY_NAME = os.getenv('API_KEY_NAME')
API_KEY_VALUE = os.getenv('API_KEY_VALUE')
API_KEY_DOMAIN = os.getenv('API_KEY_DOMAIN')

# Allowed content types for uploading
ALLOWED_CONTENT_TYPES = [
    'image/png',
    'image/jpeg',
]
