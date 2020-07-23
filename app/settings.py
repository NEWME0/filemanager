import os
import dotenv


# Load environment variables
dotenv.load_dotenv()

# Application root directory
ROOT_DIR = os.path.abspath(os.path.dirname(__name__))

# File manager root directory
HOME_DIR = os.path.join(ROOT_DIR, 'home')

# API key stuff
API_KEY_NAME = os.getenv('API_KEY_NAME')
API_KEY_VALUE = os.getenv('API_KEY_VALUE')
API_KEY_DOMAIN = os.getenv('API_KEY_DOMAIN')