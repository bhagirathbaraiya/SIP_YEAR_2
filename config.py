import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    # Flask configuration
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    DEBUG = os.environ.get('DEBUG', 'True').lower() == 'true'
    
    # Firebase configuration
    FIREBASE_CONFIG = {
        "apiKey": "AIzaSyAvW-vSwYDC63P0-OpAIx-z5FzShArXMDU",
        "authDomain": "mu-image-bot.firebaseapp.com",
        "databaseURL": "https://mu-image-bot-default-rtdb.firebaseio.com",
        "projectId": "mu-image-bot",
        "storageBucket": "mu-image-bot.firebasestorage.app",
        "messagingSenderId": "168328567080",
        "appId": "1:168328567080:web:72e2351a32f01d08dd181d",
        "measurementId": "G-7HPRX187ZR"
    }
    
    # Telegram Bot APIs
    IMAGE_BOT_API = "7871644116:AAFsjIKqD0f1uMOMcmuHVl1l-oyt2ajeVWk"
    ADMIN_BOT_API = "8060668462:AAHcpb-IE2RCl8x2YdIuYf5-YOQi64AjblE"
    
    # Admin credentials
    ADMIN_USERNAME = "test"
    ADMIN_PASSWORD = "test@2323"
    
    # ImageKit configuration
    IMAGEKIT_PUBLIC_KEY = "public_d61fy0ktXO0Sn/sFm8cb+Nvd8Wg="
    IMAGEKIT_URL_ENDPOINT = "https://ik.imagekit.io/bhagirathbaraiya"
    IMAGEKIT_AUTHENTICATION_ENDPOINT = "http://www.yourserver.com/auth"
    
    # Supabase configuration
    SUPABASE_URL = "https://jrlcwzvfbkxlceiqkrow.supabase.co"
    SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImpybGN3enZmYmt4bGNlaXFrcm93Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzczNzA4MzksImV4cCI6MjA1Mjk0NjgzOX0.uz8v3DLFm8lt5jP9NWWJiEBKLgPis63lUh9YIPh9iuA"
