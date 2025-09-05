import os
import sys
from flask import Flask, send_from_directory
from flask_cors import CORS
from src.models.user import db
from src.routes.user import user_bp
from src.routes.airfoil import airfoil_bp

# This ensures that the root of the project is on the Python path
# which is important for resolving module imports correctly.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Initialize the Flask app. By default, it serves files from a 'static' folder
# in the same directory as the app's __name__.
app = Flask(__name__, static_folder='static', static_url_path='/')

app.config['SECRET_KEY'] = 'asdf#FGSgvasgf$5$WGT'

# Enable CORS for all API routes
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Register API blueprints
app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(airfoil_bp, url_prefix='/api')

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.path.dirname(__file__), 'database', 'app.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
with app.app_context():
    db.create_all()

# Route to serve the main index.html file and other frontend assets.
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

# This block allows running the backend directly for development/testing.
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
