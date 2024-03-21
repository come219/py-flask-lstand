# config.py
## Import the Flask app instance
from server import app

# Example locations where JWT tokens might be found
app.config['JWT_TOKEN_LOCATION'] = ['headers', 'cookies']
