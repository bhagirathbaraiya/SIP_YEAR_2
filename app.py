from flask import Flask, render_template, jsonify, request, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import os
from datetime import datetime, timedelta

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
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
dummy_users = {
    1: DummyUser(1, "admin", True),
    2: DummyUser(2, "user1"),
    3: DummyUser(3, "user2")
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
    return dummy_users.get(int(user_id))

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
def users():
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

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        # Dummy authentication - accept any password
        user = next((u for u in dummy_users.values() if u.username == username), None)
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
    app.run(debug=True) 