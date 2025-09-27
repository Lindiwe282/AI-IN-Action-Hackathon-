from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///financial_coach.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')

# Initialize database
db = SQLAlchemy(app)

# Import routes
from routes.planner import planner_bp
from routes.investment import investment_bp
from routes.loan import loan_bp
from routes.literacy import literacy_bp
from routes.fraud import fraud_bp

# Register blueprints
app.register_blueprint(planner_bp, url_prefix='/api/planner')
app.register_blueprint(investment_bp, url_prefix='/api/investment')
app.register_blueprint(loan_bp, url_prefix='/api/loan')
app.register_blueprint(literacy_bp, url_prefix='/api/literacy')
app.register_blueprint(fraud_bp, url_prefix='/api/fraud')

@app.route('/')
def health_check():
    return jsonify({
        'status': 'healthy',
        'message': 'Financial Coach API is running!',
        'version': '1.0.0'
    })

@app.route('/api/health')
def api_health():
    return jsonify({
        'status': 'healthy',
        'database': 'connected',
        'services': ['planner', 'investment', 'loan', 'literacy', 'fraud']
    })

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)