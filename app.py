from flask import Flask
from models import db
from dotenv import load_dotenv
import os

# โหลดค่าจากไฟล์ .env
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///miku_sekai.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# เชื่อมต่อฐานข้อมูลกับแอปพลิเคชัน
db.init_app(app)

# สร้างไฟล์ฐานข้อมูลอัตโนมัติ
with app.app_context():
    db.create_all()

# --- Routes (หน้าเว็บต่างๆ) ---

@app.route('/')
def index():
    return "<h1>Welcome to Miku Sekai! 🎵</h1><p>โลกของคนรัก Hatsune Miku</p>"

if __name__ == '__main__':
    app.run(debug=True)