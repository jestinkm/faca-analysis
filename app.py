"""
Main Flask application for FaceSecure v2.
Clean architecture with separated services.
"""

from flask import Flask, render_template, request, jsonify
from services.face_register import register_user
from services.face_login import verify_face
from config import SECRET_KEY, DEBUG

# Initialize Flask app
app = Flask(__name__)
app.secret_key = SECRET_KEY


@app.route('/')
def index():
    """Home page."""
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    """Registration page."""
    if request.method == 'GET':
        return render_template('register.html')
    
    try:
        name = request.form.get('name')
        email = request.form.get('email')
        
        if not name or not email:
            return jsonify({'success': False, 'message': 'Name and email are required'}), 400
        
        success, message = register_user(name, email)
        
        if success:
            return jsonify({'success': True, 'message': message})
        else:
            return jsonify({'success': False, 'message': message}), 400
            
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login page."""
    if request.method == 'GET':
        return render_template('login.html')
    
    try:
        user = verify_face()
        
        if user:
            return jsonify({
                'status': 'success',
                'user': user['name'],
                'email': user['email']
            })
        else:
            return jsonify({
                'status': 'failed',
                'message': 'Face not recognized or no users registered'
            }), 401
            
    except Exception as e:
        return jsonify({'status': 'failed', 'message': str(e)}), 500


if __name__ == '__main__':
    print("Starting FaceSecure v2 application")
    app.run(debug=DEBUG, host='0.0.0.0', port=5000, use_reloader=False)
