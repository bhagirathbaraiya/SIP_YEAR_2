# Telegram Bot Admin Panel

A Flask-based admin panel for managing Telegram bots with features for group management, analytics, and settings.

## Features

- Responsive dashboard with real-time statistics
- Group management (Broadcast, User Chat, Customer Service)
- Analytics with interactive charts
- Theme support (Light/Dark mode)
- Toggleable sidebar
- Comprehensive settings management

## Requirements

- Python 3.8+
- Flask
- Flask-SQLAlchemy
- Flask-Login
- Other dependencies listed in `requirements.txt`

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd telegram-bot-admin
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Initialize the database:
```bash
flask db init
flask db migrate
flask db upgrade
```

5. Run the application:
```bash
python app.py
```

The application will be available at `http://localhost:5000`

## Usage

1. Access the dashboard at `http://localhost:5000`
2. Use the sidebar to navigate between different sections:
   - Dashboard: View statistics and recent activity
   - Groups: Manage different types of groups
   - Analytics: View detailed analytics and charts
   - Settings: Configure bot and application settings

## Security

- All sensitive data is stored securely
- Two-factor authentication support
- Session management
- Password protection for bot tokens

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.