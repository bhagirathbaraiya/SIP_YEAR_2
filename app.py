from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import os
from datetime import datetime, timedelta
from config import Config
from firebase_service import firebase_service

app = Flask(__name__)
app.config.from_object(Config)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Dummy data
class DummyUser(UserMixin):
    def __init__(self, id, username, is_admin=False):
        self.id = id
        self.username = username
        self.is_admin = is_admin

# Dummy users
users = {
    'admin': DummyUser('admin', 'admin', True),
    Config.ADMIN_USERNAME: DummyUser(Config.ADMIN_USERNAME, Config.ADMIN_PASSWORD, True)
}

# Dummy groups
groups = [
    {
        'id': 1,
        'group_name': 'Broadcast Channel',
        'group_type': 'broadcast',
        'member_count': 1500,
        'created_at': datetime.now() - timedelta(days=30)
    },
    {
        'id': 2,
        'group_name': 'User Support',
        'group_type': 'customer_service',
        'member_count': 800,
        'created_at': datetime.now() - timedelta(days=15)
    },
    {
        'id': 3,
        'group_name': 'Community Chat',
        'group_type': 'user_chat',
        'member_count': 1200,
        'created_at': datetime.now() - timedelta(days=7)
    }
]

@login_manager.user_loader
def load_user(user_id):
    return users.get(user_id)

# Routes
@app.route('/')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/groups')
@login_required
def groups_page():
    return render_template('groups.html', groups=groups)

@app.route('/analytics')
@login_required
def analytics():
    return render_template('analytics.html')

@app.route('/users')
@login_required
def users_page():
    return render_template('users.html')

@app.route('/settings')
@login_required
def settings():
    return render_template('settings.html')

@app.route('/api/stats')
@login_required
def get_stats():
    # Dummy data for demonstration
    stats = {
        'total_users': 1500,
        'active_users': 850,
        'total_groups': len(groups),
        'messages_today': 2500
    }
    return jsonify(stats)

@app.route('/api/bot-data')
@login_required
def api_bot_data():
    """API endpoint to serve bot data for dashboard"""
    try:
        # Get data from Firebase service
        data = firebase_service.get_bot_data()
        return jsonify(data)
    except Exception as e:
        print(f"Error in api_bot_data: {e}")
        # Return mock data as fallback
        return jsonify(firebase_service.get_mock_data())

@app.route('/api/users/<user_id>/status', methods=['PUT'])
@login_required
def update_user_status(user_id):
    """API endpoint to update user status"""
    try:
        data = request.get_json()
        new_status = data.get('status')
        
        if not new_status:
            return jsonify({"success": False, "message": "Status is required"}), 400
        
        result = firebase_service.update_user_status(user_id, new_status)
        return jsonify(result)
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        # Dummy authentication - check username and password
        user = None
        for u in users.values():
            if u.username == username and password == Config.ADMIN_PASSWORD:
                user = u
                break
        if user:
            login_user(user)
            return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/reports')
@login_required
def reports():
    return render_template('reports.html')

@app.route('/logs')
@login_required
def logs():
    return render_template('logs.html')

if __name__ == '__main__':
    # Get port from environment variable or default to 5000
    port = int(os.environ.get('PORT', 5000))
    # Enable debug mode and auto-reload during development
    app.run(host='0.0.0.0', port=port, debug=True) 